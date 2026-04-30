import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QPushButton, QDialog, QLabel, QLineEdit, QHBoxLayout, QCheckBox, QDateEdit, QHeaderView, QMessageBox
from PyQt5.QtCore import QTimer, Qt
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import styles

class EmployeeModification(QDialog):
    def __init__(self, employee_data):
        super().__init__()
        self.setWindowTitle("Modify Employee")
        self.setFixedSize(350, 400)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.header = QLabel("Edit Info")
        self.header.setObjectName("HeaderLabel")
        self.layout.addWidget(self.header)

        self.id_label = QLabel(f"ID: {employee_data[0]}")
        self.name_edit = QLineEdit()
        self.name_edit.setText(employee_data[1])
        self.role_edit = QLineEdit()
        self.role_edit.setText(employee_data[2])

        self.success_checkbox = QCheckBox("Update Complete")
        self.success_checkbox.setEnabled(False)

        self.update_button = QPushButton("Save Changes")
        self.update_button.clicked.connect(self.update_employee)

        self.layout.addWidget(self.id_label)
        self.layout.addWidget(QLabel("Name:"))
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(QLabel("Role:"))
        self.layout.addWidget(self.role_edit)
        self.layout.addWidget(self.success_checkbox)
        self.layout.addWidget(self.update_button)

        self.employee_id = employee_data[0]
        styles.apply_style(self)

    def update_employee(self):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="employee_db")
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("UPDATE employee SET employee_name = %s, employee_role = %s WHERE employee_id = %s",
                               (self.name_edit.text(), self.role_edit.text(), self.employee_id))
                connection.commit()
                self.success_checkbox.setChecked(True)
                QTimer.singleShot(1000, self.accept)
        except Error as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            if connection.is_connected(): connection.close()

class EmployeeManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Statistics & Management")
        self.resize(900, 700)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.header = QLabel("Management & Stats")
        self.header.setObjectName("HeaderLabel")
        self.layout.addWidget(self.header)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Role"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.graph_btn = QPushButton("Show Hours Graph")
        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.setObjectName("SecondaryButton")
        
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.graph_btn)
        self.layout.addLayout(btn_layout)

        self.graph_btn.clicked.connect(self.show_average_working_hours_graph)
        self.refresh_btn.clicked.connect(self.fetch_employee_data)

        self.fetch_employee_data()
        styles.apply_style(self)

    def fetch_employee_data(self):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="employee_db")
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT employee_id, employee_name, employee_role FROM employee")
                data = cursor.fetchall()
                self.table.setRowCount(0)
                for row_idx, row_data in enumerate(data):
                    self.table.insertRow(row_idx)
                    for col_idx, val in enumerate(row_data):
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))
        except Error as e: print(e)
        finally:
            if connection.is_connected(): connection.close()

    def show_average_working_hours_graph(self):
        # Implementation similar to HomeGui1.py
        date_dialog = QDialog(self)
        date_dialog.setWindowTitle("Select Range")
        l = QVBoxLayout(date_dialog)
        d1 = QDateEdit(); d1.setCalendarPopup(True); d1.setDate(datetime.now().date())
        d2 = QDateEdit(); d2.setCalendarPopup(True); d2.setDate(datetime.now().date())
        l.addWidget(QLabel("From:")); l.addWidget(d1)
        l.addWidget(QLabel("To:")); l.addWidget(d2)
        btn = QPushButton("Generate")
        btn.clicked.connect(date_dialog.accept)
        l.addWidget(btn)
        styles.apply_style(date_dialog)
        
        if date_dialog.exec_() == QDialog.Accepted:
            b = d1.date().toString("yyyy-MM-dd")
            e = d2.date().toString("yyyy-MM-dd")
            avg, names = calculate_average_working_hours(b, e)
            if avg:
                self.display_graph(avg, names)

    def display_graph(self, avg, names):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar([names.get(i, i) for i in avg.keys()], avg.values(), color='#3498db')
        ax.set_title("Average Hours per Employee")
        plt.xticks(rotation=30)
        fig.tight_layout()
        
        canvas = FigureCanvas(fig)
        diag = QDialog(self); diag.resize(800, 500)
        v = QVBoxLayout(diag); v.addWidget(canvas)
        styles.apply_style(diag)
        diag.exec_()

def calculate_average_working_hours(begin_date, end_date):
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="", database="employee_db")
        if connection.is_connected():
            cursor = connection.cursor()
            query = ("SELECT employee_id, MIN(timestamp), MAX(timestamp) FROM attendance "
                     "WHERE DATE(timestamp) BETWEEN %s AND %s GROUP BY employee_id, DATE(timestamp)")
            cursor.execute(query, (begin_date, end_date))
            results = cursor.fetchall()
            
            # Group by employee to get average
            emp_data = {}
            for eid, tmin, tmax in results:
                hours = (tmax - tmin).total_seconds() / 3600
                if eid not in emp_data: emp_data[eid] = []
                emp_data[eid].append(hours)
            
            avg_hours = {eid: sum(h)/len(h) for eid, h in emp_data.items()}
            
            names = {}
            for eid in avg_hours.keys():
                cursor.execute("SELECT employee_name FROM employee WHERE id = %s", (eid,))
                row = cursor.fetchone()
                names[eid] = row[0] if row else str(eid)
            
            return avg_hours, names
    except Exception as e: print(e); return {}, {}
    finally:
        if connection.is_connected(): connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmployeeManagement()
    window.show()
    sys.exit(app.exec_())