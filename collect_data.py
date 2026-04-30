import cv2
import os
from database import db

def get_last_employee_id():
    result = db.fetch_one("SELECT MAX(employee_id) FROM employee")
    try:
        return int(result[0]) if result and result[0] is not None else 0
    except (ValueError, TypeError):
        return 0

def capture_images(employee_name, employee_role):
    try:
        # Get next ID
        last_id = get_last_employee_id()
        employee_id = str(last_id + 1)

        # Directory setup
        employee_directory = f"data/{employee_id}"
        os.makedirs(employee_directory, exist_ok=True)

        # Camera setup
        video_capture = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        image_count = 0
        max_images = 30

        print(f"Starting capture for {employee_name} (ID: {employee_id})")

        while image_count < max_images:
            ret, frame = video_capture.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                image_count += 1
                face_img = frame[y:y+h, x:x+w]
                
                # Save face only
                image_path = f"{employee_directory}/image_{image_count}.jpg"
                cv2.imwrite(image_path, face_img)

                # Visual feedback
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"Capturing: {image_count}/{max_images}", (x, y-10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow('Face Registration - Stay Still', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        if image_count >= max_images:
            # Save to DB
            db.execute("INSERT INTO employee (employee_id, employee_name, employee_role) VALUES (%s, %s, %s)",
                      (employee_id, employee_name, employee_role))
            print(f"Successfully registered {employee_name}")
            return True
        else:
            print("Capture cancelled or failed.")
            return False

    except Exception as e:
        print(f"Capture Error: {e}")
        return False