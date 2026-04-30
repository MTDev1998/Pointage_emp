from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QLabel, QLineEdit, QHBoxLayout, QCheckBox
import mysql.connector
from mysql.connector import Error

class EmployeeModification(QDialog):
    def __init__(self, employee_data):
        super().__init__()

        self.setWindowTitle("Modify Employee")
        self.setGeometry(200, 200, 300, 200)

        self.layout = QVBoxLayout()

        self.employee_id_label = QLabel("Employee ID:")
        self.employee_id_value = QLabel(str(employee_data[0]))

        self.employee_name_label = QLabel("Employee Name:")
        self.employee_name_edit = QLineEdit()
        self.employee_name_edit.setText(employee_data[1])

        self.employee_role_label = QLabel("Employee Role:")
        self.employee_role_edit = QLineEdit()
        self.employee_role_edit.setText(employee_data[2])

        self.success_checkbox = QCheckBox("Modification Successful")

        self.update_button = QPushButton("Update", self)
        self.cancel_button = QPushButton("Cancel", self)

        self.update_button.clicked.connect(self.update_employee)
        self.cancel_button.clicked.connect(self.reject)

        self.layout.addWidget(self.employee_id_label)
        self.layout.addWidget(self.employee_id_value)
        self.layout.addWidget(self.employee_name_label)
        self.layout.addWidget(self.employee_name_edit)
        self.layout.addWidget(self.employee_role_label)
        self.layout.addWidget(self.employee_role_edit)
        self.layout.addWidget(self.success_checkbox)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)

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

                employee_id = self.employee_id_value.text()
                updated_name = self.employee_name_edit.text()
                updated_role = self.employee_role_edit.text()

                # Update the employee information in the database
                update_query = ("UPDATE employee "
                                "SET employee_name = %s, employee_role = %s "
                                "WHERE employee_id = %s")

                cursor.execute(update_query, (updated_name, updated_role, employee_id))
                connection.commit()

                # If the update was successful, check the checkbox
                self.success_checkbox.setChecked(True)

        except Error as e:
            print("Error:", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class EmployeeManagement(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Employee Management System")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Employee ID", "Name", "Role"])

        self.fetch_employee_data()

        self.modify_button = QPushButton("Modify Employee", self)
        self.delete_button = QPushButton("Delete Employee", self)
        self.add_button = QPushButton("Add Employee", self)

        self.modify_button.clicked.connect(self.modify_employee)
        self.delete_button.clicked.connect(self.delete_employee)
        self.add_button.clicked.connect(self.add_employee)

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.modify_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.add_button)

        self.central_widget.setLayout(self.layout)

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
                cursor.execute("SELECT employee_id,employee_name,employee_role FROM employee")

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
                self.table.setItem(row_num, col_num, item)

    def modify_employee(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            employee_data = [
                self.table.item(selected_row, 0).text(),
                self.table.item(selected_row, 1).text(),
                self.table.item(selected_row, 2).text(),
            ]

            modification_dialog = EmployeeModification(employee_data)
            if modification_dialog.exec_() == QDialog.Accepted:
                # Update the table or database if needed
                print("Modification accepted")

    def delete_employee(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            # Get the employee details from the selected row
            employee_id = self.table.item(selected_row, 0).text()
            employee_name = self.table.item(selected_row, 1).text()
            employee_role = self.table.item(selected_row, 2).text()

            # Implement the deletion logic (e.g., show a confirmation dialog)
            # For demonstration purposes, let's print the details
            print(f"Delete Employee: ID={employee_id}, Name={employee_name}, Role={employee_role}")

    def add_employee(self):
        # Implement the logic to add a new employee (You need to implement this)
        # For demonstration purposes, let's print a message
        print("Add Employee: Implement the logic to add a new employee")

if __name__ == "__main__":
    app = QApplication([])
    window = EmployeeManagement()
    window.show()
    app.exec_()
