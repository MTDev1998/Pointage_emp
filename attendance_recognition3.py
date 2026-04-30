import sys
import cv2
import face_recognition
import pickle
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from database import db
import styles

class AttendanceInfoDialog(QDialog):
    def __init__(self, name, role, timestamp):
        super().__init__()
        self.setWindowTitle("Pointage Réussi")
        self.setFixedSize(400, 250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        header = QLabel("Pointage Enregistré")
        header.setObjectName("HeaderLabel")
        header.setAlignment(Qt.AlignCenter)
        
        info_layout = QVBoxLayout()
        name_lbl = QLabel(f"<b>Employé:</b> {name}")
        role_lbl = QLabel(f"<b>Rôle:</b> {role}")
        time_lbl = QLabel(f"<b>Heure:</b> {timestamp}")
        
        info_layout.addWidget(name_lbl)
        info_layout.addWidget(role_lbl)
        info_layout.addWidget(time_lbl)

        layout.addWidget(header)
        layout.addLayout(info_layout)
        
        styles.apply_style(self)
        
        # Auto-close after 4 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.accept)
        self.timer.start(4000)

def record_attendance(internal_id):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        # 'employee_id' in the attendance table is actually a foreign key to employee.id
        db.execute("INSERT INTO attendance (employee_id, timestamp) VALUES (%s, %s)",
                  (internal_id, timestamp))
        return timestamp
    except Exception as e:
        print(f"Logging Error: {e}")
        return None

def get_employee_info(internal_id):
    # Query using the primary key 'id'
    row = db.fetch_one("SELECT employee_name, employee_role FROM employee WHERE id = %s", (internal_id,))
    return row if row else ("Inconnu", "Inconnu")

def recognize_attendance():
    # Load model
    try:
        with open("face_encodings.pkl", "rb") as f:
            known_encodings, known_ids = pickle.load(f)
    except FileNotFoundError:
        print("Error: No training data found. Please run Training first.")
        return

    # We need a hidden QApplication to show our PyQt5 dialogs
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    video_capture = cv2.VideoCapture(0)
    
    current_recognized_id = None
    current_recognized_info = None

    print("Reconnaissance activée.")
    print("-> Appuyez sur 'P' pour pointer l'employé détecté.")
    print("-> Appuyez sur 'Q' pour quitter.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Processing optimization
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        current_recognized_id = None # Reset every frame

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            name = "Inconnu"
            
            if True in matches:
                first_match_index = matches.index(True)
                internal_id = known_ids[first_match_index]
                emp_name, emp_role = get_employee_info(internal_id)
                
                current_recognized_id = internal_id
                current_recognized_info = (emp_name, emp_role)
                name = emp_name

            # UI drawing
            top *= 4; right *= 4; bottom *= 4; left *= 4
            color = (0, 255, 0) if name != "Inconnu" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, f"{name} - [P] pour pointer", (left, top - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow('Systeme de Pointage - Camera', frame)

        key = cv2.waitKey(1) & 0xFF
        
        # Press 'P' to point
        if key == ord('p'):
            if current_recognized_id:
                name, role = current_recognized_info
                ts = record_attendance(current_recognized_id)
                if ts:
                    dialog = AttendanceInfoDialog(name, role, ts)
                    dialog.exec_()
            else:
                print("Aucun employé reconnu pour le pointage.")

        # Press 'Q' to quit
        if key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_attendance()
