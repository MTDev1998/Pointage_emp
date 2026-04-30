import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
import subprocess
import os

class Database:
    def __init__(self, host="localhost", user="root", password="", database="employee_db", port=3307):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port
        }
        # Path to the SQL file to keep updated
        self.sql_file_path = os.path.join("BD", "employee_db.sql")

    @contextmanager
    def get_cursor(self):
        connection = None
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                cursor = connection.cursor()
                yield cursor
                connection.commit()
        except Error as e:
            print(f"Database Error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_all(self, query, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def fetch_one(self, query, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def execute(self, query, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
        
        # After any execution that might change data, update the SQL file
        self.update_sql_file()

    def update_sql_file(self):
        """Dumps the current state of the database back to the employee_db.sql file."""
        try:
            # We use docker exec to run mysqldump inside the container
            # This ensures we get the exact state of the database
            container_name = "employee_db_container"
            command = [
                "docker", "exec", container_name,
                "mysqldump", "-u", self.config['user'], 
                "--no-tablespaces", # Needed for some MySQL 8 configurations
                self.config['database']
            ]
            
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
            # Ensure the BD directory exists
            os.makedirs(os.path.dirname(self.sql_file_path), exist_ok=True)
            
            with open(self.sql_file_path, "w", encoding="utf-8") as f:
                f.write(result.stdout)
                
            print(f"Successfully updated {self.sql_file_path}")
        except Exception as e:
            print(f"Warning: Could not update SQL file: {e}")

# Global instance
db = Database()
