import sqlite3


con = sqlite3.connect('./database.db')
cur = con.cursor()

def init_db():
    cur.execute("CREATE TABLE IF NOT EXISTS data(upload_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, path)")

    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, email, password)")

    cur.execute("CREATE TABLE IF NOT EXISTS write(id INTEGER PRIMARY KEY AUTOINCREMENT, date, time, city, temp, temp_feels_like, pressure, humidity, description, wind_direction, wind_speed, overcast)")


    cur.execute("CREATE TABLE IF NOT EXISTS cities(id INTEGER PRIMARY KEY AUTOINCREMENT, index_vmo, city, latitude, longitude)")
    cur.execute("CREATE TABLE IF NOT EXISTS news(id INTEGER PRIMARY KEY AUTOINCREMENT, rating, title, description)")

    d = cur.execute("""SELECT * FROM users WHERE email=1 AND password=1""").fetchone()
    if d == None:
        cur.execute("""INSERT INTO users(email,password) VALUES('1','1')""")
        con.commit()
    
init_db()