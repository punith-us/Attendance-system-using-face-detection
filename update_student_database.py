#this is a python script to update the database using msql queries to update the student table


import mysql.connector # type: ignore


#database details FOR LATER DEVELOPMENT 
mydb = mysql.connector.connect(
    host = "localhost",
    user= "root",
    password="punith123",
    database="STUDENTDB"
)

mycursor = mydb.cursor()


def update_student_table(name,usn):
     sql = "INSERT INTO STUDENT (NAME,USN) VALUES(%s,%s)"
     val = (name,usn)

     mycursor.execute(sql,val)

     mydb.commit()