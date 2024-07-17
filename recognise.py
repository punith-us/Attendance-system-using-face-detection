# recognize_faces.py
import cv2
import numpy as np
import face_recognition
import pickle
import mysql.connector # type: ignore
import datetime 
import csv



#global variables
today_date = datetime.date.today()
usn_list=[]

#database details FOR LATER DEVELOPMENT 
mydb = mysql.connector.connect(
    host = "localhost",
    user= "root",
    password="punith123",
    database="STUDENTDB"
)

mycursor = mydb.cursor()

#FUNC TO EXPORT [HERE WE ARE JOINING THE NAME FROM STUDENT TABLE AND REST OF DETAILS FROM ATTENDANCE TABLE]
def export_data():
    sql_query = "SELECT A.SL_NO,A.USN,S.NAME,A.DATE,A.CHECK_IN_TIME FROM ATTENDANCE A JOIN STUDENT S ON A.USN=S.USN"
    mycursor.execute(sql_query)
    rows = mycursor.fetchall()
    csv_file='exported_data.csv'
    with open(csv_file,mode='w',newline='')as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in mycursor.description])
        writer.writerows(rows)
    print(f"DATA EXPORTED TO {csv_file} SUCCESSFULLY")


#func to update the database with attendance

def update_attendance(date,usn,status,present_time):
     sql = "INSERT INTO ATTENDANCE (DATE,USN,STATUS,CHECK_IN_TIME) VALUES(%s,%s,%s,%s)"
     val = (date,usn,status,present_time)

     mycursor.execute(sql,val)

     mydb.commit()


def load_encodings(encodings_file):
    with open(encodings_file, 'rb') as f:
        return pickle.load(f)

encodings_file = 'face_encodings.pkl'






print(f"Loading encodings from {encodings_file}...")
known_faces, known_names = load_encodings(encodings_file)
print("Encodings loaded.")

# Initialize the webcam feed
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        usn = "Unknown"
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            usn = known_names[best_match_index] # we get the names here
            if usn not in usn_list:
                print(usn)# remove later
                usn_list.append(usn)
                present_time=datetime.datetime.now().time().strftime("%H:%M:%S")      
                update_attendance(date=today_date,usn=usn,status="Present",present_time=present_time)


            
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, usn, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    cv2.imshow('Faces', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

export_data()
cap.release()
mycursor.close()
mydb.close()
cv2.destroyAllWindows()
