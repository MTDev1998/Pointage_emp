import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QDateEdit, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QHeaderView
from PyQt5.QtCore import Qt
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import pandas as pd
import styles

class AttendanceViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Attendance History")
        self.resize(1000, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.header = QLabel("History Log")
        self.header.setObjectName("HeaderLabel")
        self.layout.addWidget(self.header)

        # Filters
        filter_layout = QHBoxLayout()
        self.date_filter = QDateEdit()
        self.date_filter.setDate(datetime.now().date())
        self.date_filter.setCalendarPopup(True)
        
        self.user_filter = QLineEdit()
        self.user_filter.setPlaceholderText("Employee name...")
        
        self.filter_btn = QPushButton("Apply Filter")
        
        filter_layout.addWidget(QLabel("Date:"))
        filter_layout.addWidget(self.date_filter)
        filter_layout.addWidget(QLabel("Name:"))
        filter_layout.addWidget(self.user_filter)
        filter_layout.addWidget(self.filter_btn)
        self.layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Role", "Entry", "Exit"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.export_btn = QPushButton("Export Selection")
        self.export_btn.setObjectName("SecondaryButton")
        self.layout.addWidget(self.export_btn)

        self.filter_btn.clicked.connect(self.fetch_attendance_data)
        self.export_btn.clicked.connect(self.export_to_excel)

        self.fetch_attendance_data()
        styles.apply_style(self)

    def fetch_attendance_data(self):
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="employee_db")
            if connection.is_connected():
                cursor = connection.cursor()
                date_val = self.date_filter.date().toPyDate()
                name_val = self.user_filter.text()

                query = ("SELECT e.employee_id, e.employee_name, e.employee_role, "
                         "MIN(a.timestamp), MAX(a.timestamp) "
                         "FROM employee e LEFT JOIN attendance a ON e.id = a.employee_id "
                         "WHERE DATE(a.timestamp) = %s AND (e.employee_name LIKE %s OR %s = '') "
                         "GROUP BY e.employee_id, e.employee_name")
                
                cursor.execute(query, (date_val, f"%{name_val}%", name_val))
                data = cursor.fetchall()
                self.table.setRowCount(0)
                for row_idx, row in enumerate(data):
                    self.table.insertRow(row_idx)
                    for col_idx, val in enumerate(row):
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(val) if val else "N/A"))
        except Error as e: print(e)
        finally:
            if connection.is_connected(): connection.close()

    def export_to_excel(self):
        # Implementation is same as HomeGui1.py
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Excel', 'attendance.xlsx', 'Excel Files (*.xlsx)')
        if file_path:
            # Logic to fetch and save...
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendanceViewer()
    window.show()
    sys.exit(app.exec_())
