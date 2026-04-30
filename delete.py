import os
import shutil
from database import db

def delete_employee(employee_id):
    try:
        # Get employee name for logging
        result = db.fetch_one("SELECT employee_name FROM employee WHERE employee_id = %s", (employee_id,))
        
        if result:
            employee_name = result[0]

            # 1. Delete from Database
            db.execute("DELETE FROM employee WHERE employee_id = %s", (employee_id,))
            # Also delete attendance records for this employee to maintain integrity
            db.execute("DELETE FROM attendance WHERE employee_id = %s", (employee_id,))

            # 2. Delete File Data
            employee_directory = f"data/{employee_id}"
            if os.path.exists(employee_directory):
                shutil.rmtree(employee_directory)
                print(f"Directory {employee_directory} removed.")

            print(f"Successfully deleted {employee_name} (ID: {employee_id}) and all associated records.")
            return True
        else:
            print(f"No employee found with ID: {employee_id}")
            return False

    except Exception as e:
        print(f"Delete Error: {e}")
        return False

if __name__ == "__main__":
    # For testing:
    # delete_employee("some_id")
    pass
