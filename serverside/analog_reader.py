import datetime
import pandas as pd
import sqlite3
from numpy import NaN as nn




def read_city_and_date(city,date):

       con = sqlite3.connect('database.db')
       cur = con.cursor()


       result = cur.execute("""SELECT * FROM write WHERE city = ? AND date = ?""", (city,date,)).fetchall()

       if result == None:
              return None
       else:
              return result




def our_dataframe(date,time,city,temp,pressure,humidity,wind_speed,temp_feels_like=None,wind_direction=None,description=None,overcast=None)->pd.DataFrame:

       NaNList = [nn]*len(date)

       result = pd.DataFrame()

       if type(temp_feels_like) != pd.Series:
              temp_feels_like = NaNList.copy()
       if type(wind_direction) != pd.Series:
              wind_direction = NaNList.copy()
       if type(description) != pd.Series:
              description = NaNList.copy()
       if type(overcast) != pd.Series:
              overcast = NaNList.copy()

       result['date'] = date
       result['time'] = time
       result['city'] = city
       result['temp'] = temp
       result['temp_feels_like'] = temp_feels_like
       result['pressure'] = pressure
       result['humidity'] = humidity
       result['description'] = description
       result['wind_direction'] = wind_direction
       result['wind_speed'] = wind_speed
       result['overcast'] = overcast

       print("Resulting dataframe:",result[:5])
       return result
       
def write_listframe(listik:list):
       con = sqlite3.connect("./database.db")

       cur = con.cursor()

       cur.execute("""INSERT INTO write(date,time,city,temp,temp_feels_like,pressure,humidity,description,wind_direction,wind_speed,overcast) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                     (listik[0],listik[1],listik[2],listik[3],listik[4],listik[5],listik[6],listik[7],listik[8],listik[9],listik[10],))

       con.commit()

def write_dataframe(df:pd.DataFrame):
       con = sqlite3.connect("./database.db")


       df.to_sql('write', con, if_exists='append',index=False)

       # cur.execute("""INSERT INTO write(date,time,city,temo,temp_feels_like,pressure,humidity,desciption,wind_direction,wind_speed,overcast)""",
       #             (df['date'], df['time'], df['city'], df))

       con.commit()

def dataframe_replace_vmo(df:pd.DataFrame):
       con = sqlite3.connect("./database.db")
       cur = con.cursor()
       vmo = df['синоптический_индекс_станции']

       
       resultDF = pd.DataFrame(columns=df.columns)

       cities = []

       for i in set(list(vmo)):
              r= cur.execute("SELECT * FROM cities WHERE index_vmo = ?", (i,)).fetchone()
              if r != None:
                     leni = len(df[df['синоптический_индекс_станции'] == i])
                     resultDF = pd.concat([resultDF, df[df['синоптический_индекс_станции'] == i]])
                     cities += [r[2]]*leni
                     
       resultDF['город'] = cities
       resultDF.drop(['синоптический_индекс_станции'], axis=1, inplace=True)
       return resultDF

def do_analog_read(test:pd.DataFrame):

       print(test[:5])

       required_columns = ['синоптический_индекс_станции', 'время',
              'погода_между_сроками', 'направление_ветра', 'средняя_скорость_ветра',
              'сумма_осадков_за_период_между_сроками',
              'температура_воздуха_по_сухому_термометру',
              'относительная_влажность_воздуха',
              'атмосферное_давление_на_уровне_моря']


       test = test[[*required_columns]]

       date_time = test['время']
       date = []
       time = []
       for j in date_time:
              time.append(j.split()[0])
              date.append(j.split()[1])

       test['время'] = time
       test['дата'] = date
       test['темп_ощущается'] = [nn]*len(date)
       
       rdf = dataframe_replace_vmo(test)

       df = our_dataframe(rdf['дата'], rdf['время'], rdf['город'],rdf['температура_воздуха_по_сухому_термометру'], rdf['атмосферное_давление_на_уровне_моря'],
                          rdf['относительная_влажность_воздуха'], rdf['средняя_скорость_ветра'], rdf['темп_ощущается'], rdf['направление_ветра'], rdf['погода_между_сроками'],
                          rdf['сумма_осадков_за_период_между_сроками'])
       
       write_dataframe(df)
       print("Файл успешно загружен.")
    

def date_to_bd_date(date:datetime.datetime): # 2024-02-10 YYYY-MM-DD -> (D)D.(M)M.YYYY
        
        d = str(date).split('-')

        result = []
        for i in d:
            k = i
            for j in i:
                if j != '0':
                    break
                else:
                    k = k[1:]
            result.append(k)

        return '.'.join(result[::-1])