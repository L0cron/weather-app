import sqlite3


con = sqlite3.connect('./database.db')
cur = con.cursor()

def init_db():
    cur.execute("CREATE TABLE IF NOT EXISTS data(upload_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id, path)")

    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, email, password)")


init_db()