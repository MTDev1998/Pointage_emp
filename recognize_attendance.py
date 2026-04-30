# recognize_attendance.py

import cv2
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import face_recognition
import os
import pickle

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
                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                            # Record attendance
                            cursor.execute("INSERT INTO attendance (employee_id, timestamp) VALUES (%s, %s)",
                                           (employee_id, timestamp))
                            connection.commit()

                            print(f"Attendance recorded for Employee ID: {employee_id}")

                cv2.imshow('Face Recognition', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            video_capture.release()
            cv2.destroyAllWindows()

    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    recognize_attendance()
