import pandas as pd


df = pd.read_csv('./serverside/table.csv', index_col=0, header=1)

def get_station_by_index(index:int):

    one = df[df['ИндексВМО'] == index]

    return one


print(df)