import datetime
import time
import random
import discord

class Track:
    url = ''


def true_with_chance(chance:int):
    if chance == 0:
        return False
    rand = random.randint(1,100)
    if rand <= chance:
        return True
    else:
        return False


def colorHEXint(input):
    if input[0] == "#":
        input = input[1::]
    return int(input,16)

def timeToUnix(timeInput:str) -> int: # time is in DD.MM.YYYY
    day = 0
    month = 0
    year = 2000
    arr = timeInput.split('.')
    for i in range(len(arr)):
        if i == 0:
            day = int(arr[i])
        elif i == 1:
            month = int(arr[i])
        else:
            year = int(arr[i])
    if day >= 1 and day <= 31 and month >= 1 and month <= 12:
        timeDate = datetime.datetime(year,month,day)
        return int(time.mktime(timeDate.timetuple()))
    else:
        return -1

def currentTimeUnix():
    return int(time.mktime(datetime.datetime.now().timetuple()))

def yearsInUnix(years: int):
    return 31536000 * years

def getAge(birthUnix: int):
    return int((currentTimeUnix() - birthUnix) / 31536000)


def timeAnalyzer(text:str): # 1г1д1ч1м1с
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    times = ['г','д','ч','м','с']
    cache = ''
    result = 0
    for i in text:
        if i in numbers:
            cache+=i
        elif i in times:
            if i == times[0]:
                result += 31556926* int(cache)
            elif i == times[1]:
                result += 86400*int(cache)
            elif i == times[2]:
                result += 3600*int(cache)
            elif i == times[3]:
                result += 60*int(cache)
            else:
                result+=int(cache)

            cache = ''
        else:
            return -1
    return result

def unixToDDMM(unix:int, UTC=3):
    unix+=UTC*60*60
    date = datetime.datetime.utcfromtimestamp(unix).strftime('%d.%m')
    return date

def DDMMToUnix(text:str):

    date = datetime.datetime(year = datetime.datetime.now().year, day=int(text[:2]), month=int(text[3:]))
    return int(date.timestamp())

def fillDDMM(ddmm:str):
    spl = ddmm.split('.')
    res = ''
    if len(spl[0]) == 1:
        res+= '0' + spl[0] + '.'
    else:
        res+=spl[0]+'.'
    if len(spl[1]) == 1:
        res+='0'+spl[1]
    else:
        res+=spl[1]
    return res

def getPrevDayUnix(unix:int):
    return unix-86400

def getNextDayUnix(unix:int):
    return unix+86400

def getMidnightUnix(unix:int):
    dt = datetime.datetime.fromtimestamp(unix)
    result = datetime.datetime(year=dt.year, month=dt.month, day=dt.day, hour=0, minute=0, second=0)
    return result

def diffBetweenMidnightUnix(unix:int):
    dt = getMidnightUnix(unix)
    sc = abs(unix-dt.timestamp())
    return int(sc)

def diffBetweenNextMidnightUnix(unix:int):
    t = diffBetweenMidnightUnix(unix)
    t = 24*60*60 - t
    return t



def unixToEventTime(unix:int):
    print(datetime.datetime.utcfromtimestamp(unix).strftime('%Y-%m-%dT%H:%M:%S'))
    return datetime.datetime.utcfromtimestamp(unix).strftime('%Y-%m-%dT%H:%M:%S')


def datetimeToUnix(dt: datetime.datetime)->int:
    return dt.timestamp() 


def datetimeToYMDT(dt:datetime.datetime):
    result = ''

    result+=str(dt.year)+"-"
    result+=str(dt.month)+"-"
    result+=str(dt.day)+" "
    result+=str(dt.hour)+":"
    result+=str(dt.minute)+":"
    result+=str(dt.second)



    return result



def sortDatetimesUnix(datetimes:list):
    dts = []

    for i in datetimes:
        i:datetime.datetime
        dts.append(int(i.timestamp()))

    dts.sort()
    return dts


def sortDatetimes(datetimes:list):
    dts = sortDatetimesUnix(datetimes)
    res = []
    for i in dts:
        a = datetime.datetime.fromtimestamp(i)
        s = a.day + '.' + a.month
        res.append(s)
    return res