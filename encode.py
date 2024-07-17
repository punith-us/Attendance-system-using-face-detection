# save_encodings.py
import cv2
import os
import numpy as np
import face_recognition
import pickle

def load_known_faces_from_images(dataset_path):
    known_faces = []
    known_names = []
    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        if os.path.isdir(person_path):
            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)
                try:
                    image = cv2.imread(image_path)
                    if image is None:
                        print(f"Failed to load image {image_path}")
                        continue
                    if image.ndim == 2:
                        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                    elif image.ndim == 3 and image.shape[2] == 4:
                        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
                    elif image.ndim == 3 and image.shape[2] == 3:
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    if image.dtype != np.uint8:
                        image = image.astype(np.uint8)
                    print(f"Converted image {image_path} with shape {image.shape} and dtype {image.dtype}")
                    face_encodings = face_recognition.face_encodings(image)
                    if face_encodings:
                        known_faces.append(face_encodings[0])
                        known_names.append(person_name)
                except Exception as e:
                    print(f"Error processing image {image_path}: {e}")
    return known_faces, known_names

def save_encodings(known_faces, known_names, encodings_file):
    with open(encodings_file, 'wb') as f:
        pickle.dump((known_faces, known_names), f)

if __name__ == "__main__":
    dataset_path = 'dataset'
    encodings_file = 'face_encodings.pkl'
    
    known_faces, known_names = load_known_faces_from_images(dataset_path)
    save_encodings(known_faces, known_names, encodings_file)
    
    print(f"Encodings saved to {encodings_file}")
