# attendance_recognition.py

import cv2
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import face_recognition
import os
import pickle
import tkinter as tk

def get_employee_data_from_db():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="employee_db"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Fetch employee data from the database
            cursor.execute("SELECT employee_id, employee_name, employee_role FROM employee")
            result = cursor.fetchall()

            return result

    except Error as e:
        print("Error:", e)
        return None

    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def show_info_interface(employee_name, employee_role, timestamp):
    info_root = tk.Tk()
    info_root.title("Attendance Information")

    label_name = tk.Label(info_root, text=f"Employee Name: {employee_name}", font=('Helvetica', 12), anchor="w")
    label_name.pack(fill="both")

    label_role = tk.Label(info_root, text=f"Employee Role: {employee_role}", font=('Helvetica', 12), anchor="w")
    label_role.pack(fill="both")

    label_timestamp = tk.Label(info_root, text=f"Attendance Time: {timestamp}", font=('Helvetica', 12), anchor="w")
    label_timestamp.pack(fill="both")

    info_root.after(5000, info_root.destroy)  # Close the interface after 5000 milliseconds (5 seconds)

    info_root.mainloop()



def recognize_attendance():
    encodings, names = [], []

    # Load encodings and names from the file
    try:
        with open("face_encodings.pkl", "rb") as f:
            encodings, names = pickle.load(f)
    except FileNotFoundError:
        print("Error: Face encodings file not found. Run the training script first.")
        return

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="employee_db"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            video_capture = cv2.VideoCapture(0)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            attendance_marked = False
            last_attendance_time = datetime.now()

            while True:
                ret, frame = video_capture.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    face_encoding = face_recognition.face_encodings(frame, [(y, x + w, y + h, x)])[0]

                    # Compare with known faces
                    matches = face_recognition.compare_faces(encodings, face_encoding)

                    for i, match in enumerate(matches):
                        if match:
                            employee_id = names[i]
                            employee_name = get_employee_name_by_id(employee_id)

                            # Display employee's name on the video
                            cv2.putText(frame, f"Employee: {employee_name}", (x, y - 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

                            if cv2.waitKey(1) == ord('p') and not attendance_marked:
                                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                                # Record attendance
                                cursor.execute("INSERT INTO attendance (employee_id, timestamp) VALUES (%s, %s)",
                                               (employee_id, timestamp))
                                connection.commit()

                                print(f"Attendance recorded for Employee ID: {employee_id}")

                                # Show the information interface for 5 seconds
                                show_info_interface(employee_name, get_employee_role_by_id(employee_id), timestamp)

                                attendance_marked = True
                                last_attendance_time = datetime.now()

                # Reset attendance_marked flag after 10 seconds
                if attendance_marked and (datetime.now() - last_attendance_time).seconds > 10:
                    attendance_marked = False

                # Display the video feed
                cv2.imshow('Face Recognition', frame)

                key = cv2.waitKey(1)
                if key == 27:  # 27 is the ASCII code for the 'Esc' key
                    break
                elif key == ord('p'):
                    attendance_marked = False

            video_capture.release()
            cv2.destroyAllWindows()

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def get_employee_name_by_id(employee_id):
    employee_data = get_employee_data_from_db()

    for emp_id, employee_name, employee_role in employee_data:
        if emp_id == employee_id:
            return employee_name

    return "Unknown"

def get_employee_role_by_id(employee_id):
    employee_data = get_employee_data_from_db()

    for emp_id, employee_name, employee_role in employee_data:
        if emp_id == employee_id:
            return employee_role

    return "Unknown"

if __name__ == "__main__":
    recognize_attendance()
