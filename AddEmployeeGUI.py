import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
import collect_data
import training
import styles

class AddEmployeeGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Employee")
        self.setFixedSize(450, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(15)

        # Header
        self.header = QLabel("Employee Registration")
        self.header.setObjectName("HeaderLabel")
        self.header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header)

        # Form
        self.name_label = QLabel("Full Name:")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter employee name...")

        self.role_label = QLabel("Department / Role:")
        self.role_combobox = QComboBox()
        self.role_combobox.addItems([
            "Responsable It & Data Analyste",
            "Responsable Trésorer",
            "Busness Analyste",
            "Directeur Comercial"
        ])

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(self.role_label)
        self.layout.addWidget(self.role_combobox)

        # Spacer
        self.layout.addStretch()

        # Buttons
        self.add_button = QPushButton("Register & Capture Face")
        self.add_button.clicked.connect(self.add_employee)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("SecondaryButton")
        self.cancel_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.add_button)
        self.layout.addLayout(button_layout)

        # Apply styles
        styles.apply_style(self)

    def add_employee(self):
        employee_name = self.name_edit.text().strip()
        employee_role = self.role_combobox.currentText()

        if not employee_name:
            QMessageBox.warning(self, "Warning", "Please enter a name.")
            return

        try:
            # Show information message before starting
            QMessageBox.information(self, "Camera", "The camera will open now. Please look at the camera to capture face data.", QMessageBox.Ok)
            
            # Call the method to capture images
            collect_data.capture_images(employee_name, employee_role)

            # Call the method to train the model
            training.encode_faces_and_train_model()

            QMessageBox.information(self, "Success", "Employee added and model trained successfully!", QMessageBox.Ok)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddEmployeeGUI()
    window.show()
    sys.exit(app.exec_())
