import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

class Database:
    def __init__(self, host="localhost", user="root", password="", database="employee_db"):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }

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

# Global instance
db = Database()
