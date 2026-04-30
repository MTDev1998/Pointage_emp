import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QLabel, QLineEdit, QHBoxLayout, QCheckBox, QMessageBox, QHeaderView
from PyQt5.QtCore import QTimer, Qt
import mysql.connector
from mysql.connector import Error
import delete
import styles

class EmployeeModification(QDialog):
    def __init__(self, employee_data, update_function):
        super().__init__()

        self.setWindowTitle("Modify Employee Details")
        self.setFixedSize(400, 450)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.header = QLabel("Edit Employee")
        self.header.setObjectName("HeaderLabel")
        self.layout.addWidget(self.header)

        self.employee_id_label = QLabel(f"Employee ID: {employee_data[0]}")
        self.employee_id_label.setStyleSheet("font-weight: bold; color: #3498db;")
        
        self.employee_name_label = QLabel("Name:")
        self.employee_name_edit = QLineEdit()
        self.employee_name_edit.setText(employee_data[1])

        self.employee_role_label = QLabel("Role:")
        self.employee_role_edit = QLineEdit()
        self.employee_role_edit.setText(employee_data[2])

        self.success_checkbox = QCheckBox("Changes Saved")
        self.success_checkbox.setEnabled(False)

        self.update_button = QPushButton("Update Info")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("SecondaryButton")

        self.update_button.clicked.connect(self.update_employee)
        self.cancel_button.clicked.connect(self.reject)

        self.layout.addWidget(self.employee_id_label)
        self.layout.addWidget(self.employee_name_label)
        self.layout.addWidget(self.employee_name_edit)
        self.layout.addWidget(self.employee_role_label)
        self.layout.addWidget(self.employee_role_edit)
        self.layout.addWidget(self.success_checkbox)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.cancel_button)
        btn_layout.addWidget(self.update_button)
        self.layout.addLayout(btn_layout)

        self.employee_id = employee_data[0]
        self.update_function = update_function
        
        styles.apply_style(self)

    def update_employee(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="employee_db"
            )

            if connection.is_connected():
                cursor = connection.cursor()

                updated_name = self.employee_name_edit.text()
                updated_role = self.employee_role_edit.text()

                update_query = ("UPDATE employee "
                                "SET employee_name = %s, employee_role = %s "
                                "WHERE employee_id = %s")

                cursor.execute(update_query, (updated_name, updated_role, self.employee_id))
                connection.commit()

                self.success_checkbox.setChecked(True)
                QMessageBox.information(self, "Success", "Employee updated successfully")

                QTimer.singleShot(1500, self.accept)
                self.update_function()

        except Error as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class EmployeeManagement(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Employee Management System")
        self.resize(800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.header = QLabel("Employee Directory")
        self.header.setObjectName("HeaderLabel")
        self.layout.addWidget(self.header)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Full Name", "Department / Role"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)

        self.layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_button = QPushButton("Add New")
        self.modify_button = QPushButton("Modify Selected")
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setObjectName("DangerButton")

        self.modify_button.clicked.connect(self.modify_employee)
        self.delete_button.clicked.connect(self.delete_employee)
        self.add_button.clicked.connect(self.add_employee)

        btn_layout.addWidget(self.add_button)
        btn_layout.addWidget(self.modify_button)
        btn_layout.addWidget(self.delete_button)
        self.layout.addLayout(btn_layout)

        self.fetch_employee_data()
        styles.apply_style(self)

    def fetch_employee_data(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="employee_db"
            )

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT employee_id, employee_name, employee_role FROM employee")
                employee_data = cursor.fetchall()
                self.populate_table(employee_data)

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
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)

    def modify_employee(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            employee_data = [
                self.table.item(selected_row, 0).text(),
                self.table.item(selected_row, 1).text(),
                self.table.item(selected_row, 2).text(),
            ]
            dialog = EmployeeModification(employee_data, self.fetch_employee_data)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "Selection Required", "Please select an employee to modify.")

    def delete_employee(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            employee_id = self.table.item(selected_row, 0).text()
            name = self.table.item(selected_row, 1).text()
            
            reply = QMessageBox.question(self, 'Delete Confirmation', 
                                         f"Are you sure you want to delete {name}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                delete.delete_employee(employee_id)
                self.fetch_employee_data()
        else:
            QMessageBox.warning(self, "Selection Required", "Please select an employee to delete.")

    def add_employee(self):
        try:
            subprocess.Popen(["python", "AddEmployeeGUI.py"])
            # We don't close this window, just open the other one
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open Add Employee window: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmployeeManagement()
    window.show()
    sys.exit(app.exec_())
