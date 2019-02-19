from flask import Flask, request, render_template

import pymysql, pymysql.cursors
import csv
import numpy as np
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import errorcode
import os

app = Flask(__name__)

user='ad'
password='8'
host='m'
database='c'
conn = mysql.connector.connect(user='', password='M8', host='azm', port=3306, database='', ssl_ca='/crt.pem', ssl_verify_cert='true')

cursor = conn.cursor()

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
UPLOAD_FOLDER = dir_path

ALLOWED_EXTENSIONS = set(['txt', 'csv','xls'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




directory = "/home/yud/"



@app.route('/')
def home():

    querycd = """select DISTINCT Course from classes"""
    cursor.execute(querycd)
    datacd = cursor.fetchall()
    cd = [dict(coursenumber=row[0])
                         for row in datacd]

    return render_template("index.html", cd=cd)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        print(request.form.get('comment'))
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            '<h1>Unsuccesfull</h1>'

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            '<h1>Unsuccesfull</h1>'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)

            data = directory + filename
            print("data"+ data)


            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '<h1>Succesfull</h1>'

    return '<h1>Unsuccesfull</h1>'

@app.route('/createDB', methods=['POST'])
def createDB():
    tablename = request.form['table_name']

    # file_name = '/Users/Yatharth/Downloads/cloud/'+tablename+'.csv'
    file_name = '/home/yatharth1908/cloud/' + tablename + '.csv'
    f_obj = open(file_name, 'r')
    reader = csv.reader(f_obj)

    headers = next(reader, None)
    print(headers)


    if request.form['click'] == 'Create Table':
    # Table Create
        create_query = 'Create table IF NOT EXISTS ' + database + '.' + tablename + ' ( '
        for heading in headers:
            create_query += heading + " varchar(1000) DEFAULT NULL,"

        create_query = create_query[:-1]
        create_query += ")"
        print(create_query)
        cursor.execute(create_query)
        print('Table Created')

        print(file_name)
        print("loding insert query")
        # Load Data via CSV File
        insert_query = """LOAD DATA LOCAL INFILE '""" +file_name+ """' INTO TABLE """+tablename+""" FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'LINES TERMINATED BY '\n' IGNORE 1 LINES"""
        print("insert query executed")
        cursor.execute(insert_query)
        conn.commit()

        return 'Table Created with Uploaded Schema'

@app.route('/search', methods=['GET', 'POST'])
def search():

    subject = request.form['subject']
    coursenumber_select = request.form['coursenumber_select']
    coursenumber = request.form['coursenumber']
    coursecareer = request.form['cousecareer']

    query_tbe = ''
    toe = 0
    print(subject)
    if subject == "CSE":

        if coursecareer == "undergraduate" and not coursenumber:
            query= """select Subject, CourseNumber, SectionNumber, ClassNumber, MaxEnroll from CSEFall2018 where CourseNumber < 5000 """

            query_tbe = query
            print(query_tbe)

        elif coursecareer == "graduate" and not coursenumber:
            query = """select Subject, CourseNumber, SectionNumber, ClassNumber, MaxEnroll from CSEFall2018 where CourseNumber > 5000 """
            query_tbe = query
            print(query_tbe)

        elif coursenumber_select == "greater":
            query = """select Subject, CourseNumber, SectionNumber, ClassNumber, MaxEnroll from CSEFall2018 where CourseNumber >  """ + coursenumber + """  """
            query_tbe = query
            print(query_tbe)

        elif coursenumber_select == "less":
            query = """select Subject, CourseNumber, SectionNumber, ClassNumber, MaxEnroll from CSEFall2018 where CourseNumber <  """ + coursenumber + """  """
            query_tbe = query
            print(query_tbe)

    print(query_tbe)

    cursor.execute(query_tbe)
    data2 = cursor.fetchall()


    return str(data2)

@app.route('/searchcd', methods=['GET', 'POST'])
def searchcd():
    cdnum = request.form["coursenum"]
    querycd = """select Section, Instructor, Room from classes where Course = """ + cdnum + """ """
    cursor.execute(querycd)
    datacdet = cursor.fetchall()
    er = [dict(section=row[0],
        instructor = row[1], room = row[2])
                         for row in datacdet]

    return render_template("view.html", er=er)

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    return "You have been enrolled"

if __name__ == '__main__':
  app.run(host = "0.0.0.0", port=5000, debug = "True")
