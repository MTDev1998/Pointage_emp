import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QDateEdit, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QHeaderView, QDialog
from PyQt5.QtCore import Qt
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import Statistic
import styles

class AttendanceViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Attendance Records")
        self.resize(1000, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Header
        self.header = QLabel("Attendance Management")
        self.header.setObjectName("HeaderLabel")
        self.layout.addWidget(self.header)

        # Filter Section
        filter_group = QWidget()
        filter_group.setStyleSheet("background-color: #2a2a3d; border-radius: 10px; padding: 10px;")
        filter_layout = QHBoxLayout(filter_group)

        self.date_filter = QDateEdit()
        self.date_filter.setDate(datetime.now().date())
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setFixedWidth(150)

        self.user_filter = QLineEdit()
        self.user_filter.setPlaceholderText("Filter by name...")

        self.role_filter = QLineEdit()
        self.role_filter.setPlaceholderText("Filter by role...")

        self.filter_button = QPushButton("Search")
        self.filter_button.setFixedWidth(100)

        filter_layout.addWidget(QLabel("Date:"))
        filter_layout.addWidget(self.date_filter)
        filter_layout.addWidget(QLabel("Name:"))
        filter_layout.addWidget(self.user_filter)
        filter_layout.addWidget(QLabel("Role:"))
        filter_layout.addWidget(self.role_filter)
        filter_layout.addWidget(self.filter_button)

        self.layout.addWidget(filter_group)

        # Action Buttons
        action_layout = QHBoxLayout()
        self.export_button = QPushButton("Export to Excel")
        self.export_button.setObjectName("SecondaryButton")
        self.average_hours_button = QPushButton("View Working Hours Graph")
        
        action_layout.addWidget(self.export_button)
        action_layout.addWidget(self.average_hours_button)
        action_layout.addStretch()
        self.layout.addLayout(action_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Role", "First Entry", "Last Entry"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        
        self.layout.addWidget(self.table)

        # Connections
        self.date_filter.dateChanged.connect(self.fetch_attendance_data)
        self.filter_button.clicked.connect(self.fetch_attendance_data)
        self.export_button.clicked.connect(self.export_to_excel)
        self.average_hours_button.clicked.connect(self.show_average_working_hours_graph)

        self.fetch_attendance_data()
        styles.apply_style(self)

    def fetch_attendance_data(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="employee_db"
            )

            if connection.is_connected():
                cursor = connection.cursor()

                selected_date = self.date_filter.date().toPyDate()
                user_f = self.user_filter.text()
                role_f = self.role_filter.text()

                query = ("SELECT e.employee_id, e.employee_name, e.employee_role, "
                         "MIN(a.timestamp) AS min_time, MAX(a.timestamp) AS max_time "
                         "FROM employee e LEFT JOIN attendance a ON e.id = a.employee_id "
                         "WHERE DATE(a.timestamp) = %s "
                         "AND (e.employee_name LIKE %s OR %s = '') "
                         "AND (e.employee_role LIKE %s OR %s = '') "
                         "GROUP BY e.employee_id, e.employee_name, e.employee_role")

                cursor.execute(query, (selected_date, f"%{user_f}%", user_f, f"%{role_f}%", role_f))
                attendance_data = cursor.fetchall()
                self.populate_table(attendance_data)

        except Error as e:
            print("Error:", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def populate_table(self, data):
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(data):
            self.table.insertRow(row_num)
            for col_num, value in enumerate(row_data):
                val = str(value) if value is not None else "N/A"
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)

    def export_to_excel(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="employee_db"
            )

            if connection.is_connected():
                cursor = connection.cursor()
                selected_date = self.date_filter.date().toPyDate()
                user_f = self.user_filter.text()
                role_f = self.role_filter.text()

                query = ("SELECT e.employee_id, e.employee_name, e.employee_role, "
                         "MIN(a.timestamp) AS min_time, MAX(a.timestamp) AS max_time "
                         "FROM employee e LEFT JOIN attendance a ON e.id = a.employee_id "
                         "WHERE DATE(a.timestamp) = %s "
                         "AND (e.employee_name LIKE %s OR %s = '') "
                         "AND (e.employee_role LIKE %s OR %s = '') "
                         "GROUP BY e.employee_id, e.employee_name, e.employee_role")

                cursor.execute(query, (selected_date, f"%{user_f}%", user_f, f"%{role_f}%", role_f))
                attendance_data = cursor.fetchall()

                df = pd.DataFrame(attendance_data, columns=["ID", "Name", "Role", "Entry Time", "Exit Time"])
                file_path, _ = QFileDialog.getSaveFileName(self, 'Save Report', f'attendance_{selected_date}.xlsx', 'Excel Files (*.xlsx)')

                if file_path:
                    df.to_excel(file_path, index=False)
                    QMessageBox.information(self, "Export Success", f"Report saved to {file_path}")

        except Error as e:
            QMessageBox.critical(self, "Export Error", f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def show_average_working_hours_graph(self):
        date_dialog = QDialog(self)
        date_dialog.setWindowTitle("Select Date Range")
        date_dialog.setFixedSize(300, 250)

        layout = QVBoxLayout(date_dialog)
        
        start_date = QDateEdit()
        start_date.setCalendarPopup(True)
        start_date.setDate(datetime.now().date())
        
        end_date = QDateEdit()
        end_date.setCalendarPopup(True)
        end_date.setDate(datetime.now().date())

        layout.addWidget(QLabel("Start Date:"))
        layout.addWidget(start_date)
        layout.addWidget(QLabel("End Date:"))
        layout.addWidget(end_date)

        select_btn = QPushButton("Generate Graph")
        select_btn.clicked.connect(date_dialog.accept)
        layout.addWidget(select_btn)

        styles.apply_style(date_dialog)

        if date_dialog.exec_() == QDialog.Accepted:
            begin_str = start_date.date().toString("yyyy-MM-dd")
            end_str = end_date.date().toString("yyyy-MM-dd")
            
            avg_hours, names = Statistic.calculate_average_working_hours(begin_str, end_str)
            if avg_hours:
                self.display_graph(avg_hours, names)
            else:
                QMessageBox.information(self, "No Data", "No attendance records found for this period.")

    def display_graph(self, average_working_hours, employee_names):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ids = list(average_working_hours.keys())
        hours = list(average_working_hours.values())
        labels = [employee_names.get(eid, f'ID {eid}') for eid in ids]

        bars = ax.bar(labels, hours, color='#3498db')
        ax.set_ylabel('Avg Hours')
        ax.set_title('Average Daily Working Hours')
        plt.xticks(rotation=45, ha='right')

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}h', va='bottom', ha='center', color='white')

        fig.tight_layout()

        canvas = FigureCanvas(fig)
        graph_dialog = QDialog(self)
        graph_dialog.setWindowTitle("Statistics Visualizer")
        graph_dialog.resize(800, 600)
        
        g_layout = QVBoxLayout(graph_dialog)
        g_layout.addWidget(canvas)
        
        styles.apply_style(graph_dialog)
        graph_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendanceViewer()
    window.show()
    sys.exit(app.exec_())
