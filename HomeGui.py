import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import styles

class AttendanceHome(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Attendance System - Premium")
        self.setFixedSize(500, 600)
        
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main Layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignCenter)

        # Header
        self.header = QLabel("Attendance System")
        self.header.setObjectName("HeaderLabel")
        self.header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header)

        # Subtitle
        self.subtitle = QLabel("Welcome back! Please select an option below.")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("color: #b9bbbe; font-size: 14px; margin-bottom: 20px;")
        self.layout.addWidget(self.subtitle)

        # Buttons
        self.btn_about_user = self.create_button("About User", "images/user.png", self.add_user)
        self.btn_mark_attendance = self.create_button("Mark Attendance", "images/attendance-1.png", self.mark_attendance)
        self.btn_show_details = self.create_button("Show Details", "images/team-attendance.png", self.show_attendance_details)

        self.layout.addWidget(self.btn_about_user)
        self.layout.addWidget(self.btn_mark_attendance)
        self.layout.addWidget(self.btn_show_details)

        # Footer
        self.footer = QLabel("© 2026 Attendance Management System")
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setStyleSheet("color: #44445c; font-size: 11px; margin-top: 30px;")
        self.layout.addWidget(self.footer)

        # Apply Global Style
        styles.apply_style(self)

    def create_button(self, text, icon_path, callback):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(60)
        
        # Try to load icon
        try:
            icon = QIcon(icon_path)
            if not icon.isNull():
                btn.setIcon(icon)
                btn.setIconSize(QSize(30, 30))
        except:
            pass
            
        btn.clicked.connect(callback)
        return btn

    def add_user(self):
        try:
            subprocess.Popen(["python", "updateGUI.py"])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open User Management: {e}")

    def mark_attendance(self):
        try:
            subprocess.Popen(["python", "attendance_recognition3.py"])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not start attendance recognition: {e}")

    def show_attendance_details(self):
        try:
            subprocess.Popen(["python", "HomeGui1.py"])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not show attendance details: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendanceHome()
    window.show()
    sys.exit(app.exec_())
