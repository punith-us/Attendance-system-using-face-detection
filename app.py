from flask import Flask,request,render_template,redirect,url_for,flash,Response
from datetime import datetime
from werkzeug.utils import secure_filename # to make sure the name of file does not contain unecessary characters

import os
import subprocess
import update_student_database
import cv2
import mysql.connector


#database details FOR LATER DEVELOPMENT 
mydb = mysql.connector.connect(
    host = "localhost",
    user= "root",
    password="punith123",
    database="STUDENTDB"
)
cursor= mydb.cursor()


app= Flask(__name__)
app.secret_key = "supersecretkey"
#for student registartion
app.config['UPLOAD_FOLDER']= '/Users/pus/VSCODE/face-project/dataset'
app.config['ALLOWED_EXTENSIONS']={'jpeg','jpg','JPG'}




#check if directory is present else make the directory here the app.config['UPLOAD_FOLDER'] is the name of the folder
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']   # we trim after the . in the filename and match to jpeg and jpg

@app.route("/") #decorator mentioning the url path to app
def home():
    return render_template('index.html')


@app.route('/attendance_details', methods =['GET','POST']) 
def attendance_details():
    if request.method=='POST':
        date=request.form['date']
        start_time=request.form['start_time']  
        end_time=request.form['end_time']   
         
       
            # Parse the input time string into a datetime object
        parsed_start_time = datetime.strptime(start_time, '%H:%M:%S').time()
            # Format the time object as a string in MySQL TIME format
        formatted_start_time = parsed_start_time.strftime('%H:%M:%S')  

         # Parse the input time string into a datetime object
        parsed_end_time = datetime.strptime(end_time, '%H:%M:%S').time()
            # Format the time object as a string in MySQL TIME format
        formatted_end_time = parsed_end_time.strftime('%H:%M:%S')  




        print(date,start_time,end_time)
       
        query='SELECT A.*,S.NAME  FROM ATTENDANCE A JOIN STUDENT S ON A.USN=S.USN WHERE DATE = %s AND CHECK_IN_TIME BETWEEN %s AND %s '
        cursor.execute(query,(date,formatted_start_time,formatted_end_time))
        attendance_data = cursor.fetchall()
        print(attendance_data)

        return render_template('attendance_details.html', data=attendance_data)

    return render_template('attendance_form.html')

        


@app.route('/add_user',methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        usn= request.form['usn']
        files= request.files.getlist('file') #get the list of uplaoded files

        if files: # if the files exist 
            usn_folder = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(usn))
            if not os.path.exists(usn_folder):
              os.makedirs(usn_folder)


            for file in files:
            
                if file and allowed_file(file.filename): 
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(usn_folder,filename)
                    file.save(file_path)

                else:
                    flash(f'inavlid file format for the file {file.filename}. only jpg and jpeg files are allowed')

            
            flash('user added successfully')

            # update the databse by calling the update_student_database.py 
            update_student_database.update_student_table(name=name,usn=usn)
            #run the bash script to encode 
            bash_script = './run_encode_script.sh'

            # Run the Bash script using subprocess
            try:
               subprocess.run(['bash', bash_script], check=True)
            except subprocess.CalledProcessError as e:
               print(f"Error running Bash script: {e}")

            return redirect(url_for('add_student'))
        
        else:
            flash('no files were uploaded')
            return redirect(request.url) # url of the current reuqest is request.url
    
    return render_template('add_user_beautiful.html')


@app.route('/monitor')
def monitor():
           
    #run the bash script to encode 
    bash_script = './run_recognise_script.sh'

    # Run the Bash script using subprocess
    try:
       subprocess.run(['bash', bash_script], check=True)
    except subprocess.CalledProcessError as e:
               print(f"Error running Bash script: {e}")
           
    return render_template('monitor.html')  

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)