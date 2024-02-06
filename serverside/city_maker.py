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

print(cities[:2])

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

for j in range(len(rlatitude)):
    geo = {'format': 'json', 'lat': f'{rlatitude[j]}', 'lon': f'{rlongitude[j]}'}
    r = requests.get('https://nominatim.openstreetmap.org/reverse', params=geo)


    bytes_str = r.content
    dict_str = bytes_str.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    print(mydata['display_name'])
    
    all_cities.append(mydata['display_name'].split(', '))
    time.sleep(1)
    if j == 3:
        break


ndf = pd.DataFrame()

ndf.columns = ['station_name', 'city_index', 'displaye_name']