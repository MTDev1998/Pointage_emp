import face_recognition
import os
import pickle
from database import db

def encode_faces_and_train_model():
    print("Training model started...")
    
    # Fetch all employees - we need 'id' for attendance records and 'employee_id' for folders
    employees = db.fetch_all("SELECT id, employee_id, employee_name FROM employee")
    
    if not employees:
        print("No employees found in database.")
        return False

    known_encodings = []
    known_ids = []

    for internal_id, custom_id, name in employees:
        folder_path = f"data/{custom_id}"
        
        if not os.path.exists(folder_path):
            print(f"Warning: No data folder for {name} (ID: {custom_id})")
            continue

        print(f"Processing images for: {name}...")
        
        for filename in os.listdir(folder_path):
            if filename.endswith((".jpg", ".png", ".jpeg")):
                image_path = os.path.join(folder_path, filename)
                
                try:
                    image = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(image)
                    
                    if encodings:
                        known_encodings.append(encodings[0])
                        # IMPORTANT: Store the internal 'id' which is the foreign key for attendance
                        known_ids.append(str(internal_id))
                except Exception as e:
                    print(f"Skipping {filename}: {e}")

    if known_encodings:
        # Save to file
        with open("face_encodings.pkl", "wb") as f:
            pickle.dump((known_encodings, known_ids), f)
        print(f"Training complete. Encoded {len(known_encodings)} faces for {len(set(known_ids))} employees.")
        return True
    else:
        print("No faces were successfully encoded.")
        return False

if __name__ == "__main__":
    encode_faces_and_train_model()
