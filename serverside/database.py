import sqlite3


con = sqlite3.connect('./database.db')
cur = con.cursor()

def init_db():
    cur.execute("CREATE TABLE IF NOT EXISTS data(upload_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id, path)")

    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, email, password)")

    cur.execute("CREATE TABLE IF NOT EXISTS write(id INTEGER PRIMARY KEY AUTOINCREMENT, date, time, city, temp, temp_feels_like, pressure, humidity, description, wind_direction, wind_speed, overcast)")

init_db()