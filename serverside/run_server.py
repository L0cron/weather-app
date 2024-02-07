from flask import Flask, request, redirect, url_for, render_template, flash
import sqlite3
import requests
import os
import datetime

import pandas as pd

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


def write_file_db(user_id, path):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    cur.execute(f"""INSERT INTO data(user_id, path) VALUES(?, ?)""", (user_id, path,))
    con.commit()

def add_user_db(email, password):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    cur.execute(f"""INSERT INTO data(email, password) VALUES(?, ?)""", (email, password,))
    con.commit

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

        columns = df.columns
        return 1
    except FileNotFoundError:
        return -1
    except:
        return -2





@app.route('/analyze', methods=['GET'])
def analyze():
    email = request.args.get('email')
    password = request.args.get('password')
    if email != None and password != None:
        valid = connect_and_sign_in(email,password)

        if valid != False:
            file = request.args.get("file")
            if file != None:
                r = analyze_file("./"+file)
                if r == 1:
                    return "Analyzing"
                elif r == -1:
                    return "File not found"
                elif r == -2:
                    return "Error."
            else:
                return "No files provided"
        else:
            return "Login Failed"
        

    else:
        return "No login provided"

@app.route("/", methods=['GET', 'POST'])
def innex():
    email = request.args.get('email')
    password = request.args.get('password')

    
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
            analyze_file(j)
        return "Success"
    else:
        if email != None and password != None:
            

            valid = connect_and_sign_in(email,password)

            if valid != False:
                return "success"
            else:
                return "failed"

        else:

            city = request.args.get('city')
            if city != None:
                
                return "Searching city..."            

            else:
                return "None"



@app.route("/cities")
def cities():
    return "cities"


app.run(host='localhost')
