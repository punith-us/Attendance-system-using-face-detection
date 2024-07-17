# view_encodings.py
import pickle
import numpy as np
import pandas as pd

def load_encodings(encodings_file):
    with open(encodings_file, 'rb') as f:
        return pickle.load(f)

encodings_file = 'face_encodings.pkl'
output_file = 'face_encodings.csv'

print(f"Loading encodings from {encodings_file}...")
known_faces, known_names = load_encodings(encodings_file)
print("Encodings loaded.")

# Prepare data for DataFrame
data = []
for name, encoding in zip(known_names, known_faces):
    encoding_list = encoding.tolist()  # Convert numpy array to list
    data.append([name] + encoding_list)

# Create DataFrame
columns = ['Name'] + [f'Encoding_{i}' for i in range(len(known_faces[0]))]
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv(output_file, index=False)
print(f"Encodings saved to {output_file}")
