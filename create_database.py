import mysql.connector # type: ignore


#database details update here accordingly and assuming you know how to create database duh 
mydb = mysql.connector.connect(
    host = "localhost",
    user= "root",
    password="punith123",
    database="dummydb"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE STUDENT (NAME VARCHAR(255),USN VARCHAR(10) PRIMARY KEY)")
mycursor.execute("INSERT INTO STUDENT VALUES('STUDENT1','USN1')")
mycursor.execute("CREATE TABLE ATTENDANCE (SL_NO INTEGER(50) AUTO_INCREMENT PRIMARY KEY,DATE DATE,USN VARCHAR(10),STATUS VARCHAR(10),CHECK_IN_TIME TIME,FOREIGN KEY (USN) REFERENCES STUDENT(USN))")

mycursor.close()
mydb.close