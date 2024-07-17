import cv2
import os
import numpy as np
import face_recognition

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to load known faces and their names
def load_known_faces(dataset_path):
    known_faces = []
    known_names = []
    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        if os.path.isdir(person_path):
            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)
                try:
                    # Load the image using OpenCV
                    image = cv2.imread(image_path)
                    if image is None:
                        print(f"Failed to load image {image_path}")
                        continue
                    
                    # Ensure the image is in RGB format
                    if image.ndim == 2:  # Grayscale image
                        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                    elif image.ndim == 3 and image.shape[2] == 4:  # RGBA image
                        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
                    elif image.ndim == 3 and image.shape[2] == 3:  # Already in BGR format
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
                    # Verify the image type is correct
                    if image.dtype != np.uint8:
                        image = image.astype(np.uint8)
                    
                    # Check image properties after conversion
                    print(f"Converted image {image_path} with shape {image.shape} and dtype {image.dtype}")

                    # Get face encodings
                    face_encodings = face_recognition.face_encodings(image)
                    if face_encodings:
                        known_faces.append(face_encodings[0])
                        known_names.append(person_name)
                except Exception as e:
                    print(f"Error processing image {image_path}: {e}")
    return known_faces, known_names

# Load known faces
dataset_path = 'dataset'
known_faces, known_names = load_known_faces(dataset_path)

# Initialize the webcam feed
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Convert the frame to RGB for face_recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    # Compare each face found in the current frame to known faces
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"
        
        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]
        
        # Draw a rectangle around the face and label it
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Faces', frame)
    
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the windows
cap.release()
cv2.destroyAllWindows()
