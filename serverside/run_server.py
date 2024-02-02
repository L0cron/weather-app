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
        return True


def write_file_db(user_id, path):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    cur.execute(f"""INSERT INTO data(user_id, path) VALUES({user_id}, {path})""")

def add_user_db(email, password):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    cur.execute(f"""INSERT INTO data(email, password) VALUES({email}, {password})""")


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

        for index,row in df.iterrows():
            print(row)
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

        if valid:
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
def idnex():
    email = request.args.get('email')
    password = request.args.get('password')

    
    if request.method == "POST":
        url = request.args.get("url")
        files = request.files
        if files != None:
            print(files)
        elif url != None:
            print(url)
        print(len(files))
        for i in range(len(files)):
            if files[f"file{str(i)}"] and allowed_file(files[f"file{str(i)}"].filename):
                files[f"file{str(i)}"].save(os.path.join(app.config['UPLOAD_FOLDER'], files[f"file{str(i)}"].filename))
                print("File saved")
    else:
        if email != None and password != None:
            

            valid = connect_and_sign_in(email,password)

            if valid:
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
