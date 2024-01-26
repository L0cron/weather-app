from flask import Flask, request, redirect, url_for, render_template, flash
import sqlite3
import requests
app = Flask("Server")

def connect_and_sign_in(email, password):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    found = cur.execute(f"""SELECT * FROM users WHERE email="{email}" AND password="{password}\"""").fetchone()
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
    else:
        if email == None or password == None:
            return "None"

        valid = connect_and_sign_in(email,password)
        if valid:
            return "success"
        else:
            return "failed"








app.run(host='localhost')
