# encode_and_train_model.py

import face_recognition
import os
import mysql.connector
from mysql.connector import Error
import pickle
from sklearn.svm import SVC

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

def encode_faces_and_train_model(dataset_path):
    employee_data = get_employee_data_from_db()

    if employee_data is None:
        return

    encodings = []
    names = []

    for employee_id, employee_name, employee_role in employee_data:
        employee_folder_path = os.path.join(dataset_path, str(employee_id))

        if os.path.exists(employee_folder_path):
            for filename in os.listdir(employee_folder_path):
                image_path ="data/"+employee_id
