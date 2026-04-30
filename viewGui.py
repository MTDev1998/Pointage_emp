import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from database import db
import styles

class SimpleAttendanceView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quick Attendance View")
        self.resize(800, 500)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.header = QLabel("Daily Summary")
        self.header.setObjectName("HeaderLabel")
        self.layout.addWidget(self.header)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Role", "First Entry", "Last Entry"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.fetch_data()
        styles.apply_style(self)

    def fetch_data(self):
        query = ("SELECT e.employee_name, e.employee_role, "
                 "MIN(a.timestamp), MAX(a.timestamp) "
                 "FROM employee e LEFT JOIN attendance a ON e.id = a.employee_id "
                 "GROUP BY e.employee_name, e.employee_role")
        
        results = db.fetch_all(query)
        self.table.setRowCount(0)
        for row_idx, row in enumerate(results):
            self.table.insertRow(row_idx)
            for col_idx, val in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(val) if val else "No Data"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleAttendanceView()
    window.show()
    sys.exit(app.exec_())
