# register_employee.py

import cv2
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime

def register_employee():
    employee_name = input("Enter Employee Name: ")
    employee_role = input("Enter Employee Role: ")

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="employee_db"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Insert employee information into the database
            cursor.execute("INSERT INTO employee (employee_name, employee_role) VALUES (%s, %s)",
                           (employee_name, employee_role))
            connection.commit()

            # Get the last inserted employee_id
            cursor.execute("SELECT LAST_INSERT_ID()")
            employee_id = cursor.fetchone()[0]

            # Create a directory for the employee if not exists
            employee_directory = f"data/{employee_id}"
            os.makedirs(employee_directory, exist_ok=True)

            # Start capturing images
            video_capture = cv2.VideoCapture(0)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            image_count = 0

            while True:
                ret, frame = video_capture.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    image_count += 1
                    image_path = f"{employee_directory}/image_{image_count}.jpg"
                    cv2.imwrite(image_path, frame[y:y + h, x:x + w])

                    cv2.imshow('Face Capture', frame)

                if cv2.waitKey(1) & 0xFF == ord('q') or image_count >= 5:
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
    register_employee()
