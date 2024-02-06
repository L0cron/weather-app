import pandas as pd

import requests
import re

import ast
import time


cities = pd.read_csv("./cities.csv", index_col=0)



cities.columns = list(cities.iloc[0])
cities = cities[1:]
cities.reset_index(inplace=True)
cities.drop('index', axis=1, inplace=True)

print(cities[:5])

latitude = cities.широта
longitude = cities.долгота

rlatitude = []
rlongitude = []



for i in latitude:
    i = i.replace('о', '°').replace('o', '°').replace(' ', '°')
    deg,min = re.split('[°\'"]', i)
    min = int(min[:-1])
    rlatitude.append(float(deg) + float(min)/60)
    
for i in longitude:
    i = i.replace('о', '°').replace('o', '°').replace(' ', '°')
    deg,min = re.split('[°\'"]', i)
    min = int(min[:-1])
    rlongitude.append(float(deg) + float(min)/60)
    

print(rlatitude[0], rlongitude[0])

all_cities = []

api = '32442b1be417871ff0af3e7e5cb87db8'
def get_city(city_req, recur=1):
    try:
        r2 = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+city_req+'&units=metric&lang=ru&appid='+api, timeout=240)
        print("content is " + r2.content.decode("UTF-8"))
        
        result = ast.literal_eval(r2.content.decode("UTF-8"))

        if 'message' in result:
            print("City not found " + city)

        return result
    except requests.ReadTimeout:
        print("idk - recursim " + str(recur))
        recur += 1
        get_city(city_req, recur)
    except requests.exceptions.ConnectionError:
        print("idk - recursim " + str(recur))
        recur += 1
        get_city(city_req, recur)

for j in range(len(rlatitude)):
    geo = {'format': 'json', 'lat': f'{rlatitude[j]}', 'lon': f'{rlongitude[j]}'}
    r = requests.get('https://nominatim.openstreetmap.org/reverse', params=geo, timeout=240)



    bytes_str = r.content
    dict_str = bytes_str.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)

    city = mydata['display_name'].split(', ')[0]
    print(mydata['display_name'])
    
<<<<<<< HEAD
    all_cities.append(mydata['display_name'].split(', '))
=======
    city_req = city.replace(' ', '&')
    print(city_req)

    result = get_city(city_req)
    print(result)
    # all_cities.append(city)
    # print("timed out: " + city)
    # print("City not found: " + city)
    
    
    
>>>>>>> 7cd276aa01a06e43732c6c8c5374c3049f3e74d8
    time.sleep(1)
    if j == 3:
        break


ndf = pd.DataFrame()

ndf.columns = ['station_name', 'city_index', 'displaye_name']