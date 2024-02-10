from flask import Flask, request, redirect, url_for, render_template, flash
import sqlite3
import requests
import os
import datetime

import pandas as pd

import analog_reader

app = Flask("Server")
app.config['UPLOAD_FOLDER'] = "./uploads"
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def connect_and_sign_in(email, password):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    found = cur.execute(f"""SELECT * FROM users WHERE email=? AND password=?""",
                        (email,password,)).fetchone()
    if found == None:
        return False
    else:
        return found
    
def user_exists(email):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    found = cur.execute(f"""SELECT * FROM users WHERE email=?""",
                        (email,)).fetchone()
    if found == None:
        return False
    else:
        return True

def write_file_db(user_id, path):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    cur.execute(f"""INSERT INTO data(user_id, path) VALUES(?, ?)""", (user_id, path,))
    con.commit()

def add_user_db(email, password):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    cur.execute(f"""INSERT INTO users(email, password) VALUES(?, ?)""", (email, password,))
    con.commit()

def download_file(url):
    req = requests.request(url=url, method='GET')
    req

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS







def analyze_file(path:str):
    try:
        df = None
        if path.endswith("csv"):
            df = pd.read_csv(path, index_col=0)
        else:
            df = pd.read_excel(path, index_col=0)

        analog_reader.do_analog_read(df)
        return 1
    except FileNotFoundError:
        print("Not found.")
        return -1


@app.route("/", methods=['GET', 'POST'])
def innex():
    email = request.args.get('email')
    password = request.args.get('password')
    rpass = request.args.get("rpassword")

    
    if request.method == "POST" and email != None and password != None:
        valid = connect_and_sign_in(email,password)

        if valid == False:
            return "failed"


        url = request.args.get("url")
        files = request.files
        if files != None:
            print(files)
        elif url != None:
            print(url)
        print(len(files))

        user_id = valid[1]

        paths = []

        for i in range(len(files)):
            if files[f"file{str(i)}"] and allowed_file(files[f"file{str(i)}"].filename):
                dat = str(int(datetime.datetime.utcnow().timestamp()))
                path = os.path.join(app.config['UPLOAD_FOLDER'], dat+"_"+files[f"file{str(i)}"].filename)
                files[f"file{str(i)}"].save(path)
                paths.append(path)
                write_file_db(path=path, user_id=user_id)
                print("File saved")
                
        for j in paths:
            print("Analyzing:",j)
            analyze_file(j)
        return "Success"
    else:
        if email != None and password != None and rpass != None:
            add_user_db(email, password)
            return "success"
        elif email != None and password != None:
            

            valid = connect_and_sign_in(email,password)

            if valid != False:
                return "success"
            else:
                return "failed"

        elif email != None and password == None:

            if_exists = user_exists(email)

            if if_exists:
                return "registered"
            else:
                return "None"

        else:

            city = request.args.get('city')
            if city != None:
                
                return "Searching city..."            

            else:
                return "None"



@app.route('/files', methods=["GET"])
def files():
    email = request.args.get('email')
    password = request.args.get('password')



@app.route("/cities")
def cities():
    return "cities"


app.run(host='localhost')
