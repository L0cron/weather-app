from flask import Flask, request, redirect, url_for, render_template, flash, send_file
import sqlite3
import requests
import os
import datetime
from numpy import NaN as nn
import pandas as pd
import random
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

        user_id = valid[0]

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





@app.route("/cities")
def cities():
    con =sqlite3.connect("./database.db")
    cur = con.cursor()

    listik = cur.execute("""SELECT * FROM cities""").fetchall()

    result = []
    for i in listik:
        result.append(i[2])

    return result

@app.route('/city', methods=["GET"])
def city():

    city = request.args.get("city")
    date = request.args.get('date')

    if city == None:
        return "City and Date must be filled"
    

    result = analog_reader.read_city_and_date(city,date)
    if result == []:
        init_city(city)
        result = analog_reader.read_city_and_date(city,date)
        if result == []:
            return ['None']
        else:
            return result
    else:
        return result

@app.route('/files', methods=['GET'])
def files():
    email = request.args.get('email')
    password = request.args.get('password')

    if email == None or password == None:
        return "Email and password must be filled"
    else:
        valid = connect_and_sign_in(email,password)

        if valid == False:
            return "failed"
        

        con = sqlite3.connect("./database.db")
        cur = con.cursor()
        user_id = cur.execute("""SELECT id FROM users WHERE email=? AND password=?""",(email,password)).fetchone()[0]
        print("uid",user_id)
        user_id = int(user_id)

        listik = cur.execute("""SELECT path FROM data WHERE user_id = ?""", (user_id,)).fetchall()
        print('listik',listik)
        return listik



@app.route("/download", methods=['GET'])
def download():

    email = request.args.get('email')
    password = request.args.get('password')
    path = request.args.get("path")

    if email == None or password == None or path == None:
        return "Email, password and path must be filled in order to download file from server"


    valid = connect_and_sign_in(email,password)

    if valid:

        user_id = int(valid[0])
        file = './uploads\\' + path

        con = sqlite3.connect("./database.db")
        cur = con.cursor()


        res = cur.execute("""SELECT * FROM data WHERE user_id=? AND path=?""", (user_id,file,)).fetchone()

        if res != None:
            return send_file(file)
        else:
            return "File not found."





    else:
        return "failed"



@app.route("/data", methods=['GET'])
def data():
    date_from:str= request.args.get('from')
    date_to:str = request.args.get('to')
    city:str = request.args.get('city')

    if date_from == None or date_to == None or city == None:
        return "city, Data_from and data_to must be filled"


    date_from:datetime.date = datetime.datetime.strptime(date_from, '%d.%m.%Y')
    date_to:datetime.date = datetime.datetime.strptime(date_to, '%d.%m.%Y')
    

    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    r = cur.execute("""SELECT * FROM write WHERE city = ?""", (city,)).fetchall()

    print(date_from)
    print(date_to)

    been = []
    result = []
    for i in r:
        dt = datetime.datetime.strptime(i[1], '%d.%m.%Y')

        if date_to >= dt and dt >= date_from and not i[1] in been:
            result.append(i)
            print(i)
            been.append(i[1])

    print('been',been)
    return result





def init_city(city):
    status = 'success'
    now = datetime.datetime.now()
    date = datetime.date.today()
    time = str(now.hour) + ":" +  str(now.minute)
    date = analog_reader.date_to_bd_date(date)
    url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    
    
    weather_data = requests.get(url=url).json()
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    wind_direction = weather_data['wind']['deg']
    wind_speed = weather_data['wind']['speed']

    overcast = nn
    
    try:
        analog_reader.write_listframe([date,time,city,
                                    temp,feels_like,pressure,
                                    humidity,description,
                                    wind_direction,wind_speed,overcast])
    except:
        status = 'failed'
    print("Init", status)


def normalize_data(city,temp,pressure,humidity,wind_direction,wind_speed,dt):
    
    pass

@app.route('/predict', methods=['GET'])
def predict():

    date = request.args.get('date')

    if date == None:
        return "Date should not be None"
    date = date.split()[0]

    day = datetime.datetime.strptime(date, '%d.%m.%Y').day
    month = datetime.datetime.strptime(date, '%d.%m.%Y').month

    # Model output:
    leto = 4.5
    temp = -5.469228904092254 + leto*0.04938753*day+1.12988844*month +random.randint(3,12)
    humidity = 67.50217518013736 + leto*0.02686177 * day + 0.79692397 * month +  random.randint(-30,10)
    pressure = 989.8152541574443-0.03810141 * day*leto  +  0.61799056 * month -  random.randint(-100,300)





    return [temp,humidity,pressure]



def init_moscow():

    status = 'success'
    now = datetime.datetime.now()
    date = datetime.date.today()
    time = str(now.hour) + ":" +  str(now.minute)
    date = analog_reader.date_to_bd_date(date)
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Москва&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    
    
    weather_data = requests.get(url=url).json()
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    city = 'Москва'
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    wind_direction = weather_data['wind']['deg']
    wind_speed = weather_data['wind']['speed']

    overcast = nn
    
    try:
        analog_reader.write_listframe([date,time,city,
                                    temp,feels_like,pressure,
                                    humidity,description,
                                    wind_direction,wind_speed,overcast])
    except:
        status = 'failed'
    print("Init", status)





init_moscow()

app.run(host='localhost')
