
GLOBAL_STYLE = """
/* Global Styles */
QMainWindow, QDialog {
    background-color: #1e1e2e;
    color: #e0e0e0;
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

QWidget {
    background-color: transparent;
    color: #e0e0e0;
}

/* Labels */
QLabel {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 5px;
}

QLabel#HeaderLabel {
    font-size: 24px;
    font-weight: bold;
    color: #3498db;
    margin-bottom: 20px;
}

/* Line Edits and ComboBoxes */
QLineEdit, QComboBox, QDateEdit {
    background-color: #2a2a3d;
    border: 1px solid #44445c;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    color: #ffffff;
    selection-background-color: #3498db;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 2px solid #3498db;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #44445c;
}

/* Buttons */
QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #2471a3;
}

QPushButton#SecondaryButton {
    background-color: #44445c;
}

QPushButton#SecondaryButton:hover {
    background-color: #555570;
}

QPushButton#DangerButton {
    background-color: #e74c3c;
}

QPushButton#DangerButton:hover {
    background-color: #c0392b;
}

/* Table Widget */
QTableWidget {
    background-color: #2a2a3d;
    border: 1px solid #44445c;
    border-radius: 8px;
    gridline-color: #44445c;
}

QHeaderView::section {
    background-color: #34495e;
    color: white;
    padding: 8px;
    border: 1px solid #44445c;
    font-weight: bold;
}

QTableWidget::item {
    padding: 10px;
}

QTableWidget::item:selected {
    background-color: #3498db;
    color: white;
}

/* ScrollBars */
QScrollBar:vertical {
    border: none;
    background: #1e1e2e;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #44445c;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #3498db;
}

/* CheckBox */
QCheckBox {
    spacing: 10px;
    font-size: 14px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 1px solid #44445c;
    background-color: #2a2a3d;
}

QCheckBox::indicator:checked {
    background-color: #2ecc71;
    border-color: #27ae60;
}
"""

def apply_style(app_or_window):
    app_or_window.setStyleSheet(GLOBAL_STYLE)
