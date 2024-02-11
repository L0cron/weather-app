import pandas as pd
import sqlite3

con = sqlite3.connect('./database.db')

df = pd.read_csv(r'./cities.csv', index_col=0)


cur = con.cursor()

def write_bd(vmo,city,lat,lon):
    
    cur.execute("""INSERT INTO cities(index_vmo, city, latitude, longitude) VALUES(?,?,?,?)""", (vmo,city,lat,lon,))
    con.commit()


for i in df.iterrows():

    series = i[1]
    vmo = series.index_vmo
    city = series.city
    latitude = series.latitude
    longitute = series.longitude

    write_bd(vmo,city,latitude,longitute)