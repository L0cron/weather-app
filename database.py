import sqlite3
import discord

# DATABASE
# Code is written by Locron
# Do not copy
# Version 2

def connectDatabase():
    global base, cur
    base = sqlite3.connect("Boti.db")
    cur = base.cursor()
    if base:
        initDataBaseCheck()
        print("Database connected!")
        return True
    else:
        print("Database is not connected!")
        return False

# Adders
def addUser(id: int):
    cur.execute(f"""
                INSERT INTO users(id)
                SELECT ?
                WHERE NOT EXISTS(SELECT 1 FROM users WHERE id = ?)
    """,
    (id,id))
    base.commit()
    print("User " + str(id) + " added successfully.")

def addServer(id: int):
    cur.execute(f"""
                INSERT INTO servers(id)
                SELECT ?
                WHERE NOT EXISTS(SELECT 1 FROM servers WHERE id = ?)
    """,
    (id,id))
    base.commit()
    print("Server " + str(id) + " added successfully.")   

# Checkers
def userCheck(id: int): # Checks if user id is in DB and adds if not
    cur.execute(f"""
                INSERT INTO users(id)
                SELECT ?
                WHERE NOT EXISTS(SELECT 1 FROM users WHERE id = ?)
    """, (id,id))
    base.commit()

def serverCheck(id: int): # Checks if server id is in DB and adds if not
    cur.execute(f"""
                INSERT INTO servers(id)
                SELECT ?
                WHERE NOT EXISTS(SELECT 1 FROM servers WHERE id = ?)
    """, (id,id))
    base.commit()




# Setters
def setUserValue(id: int, key: str, value: str):
    userCheck(id)
    cur.execute(f"""
                UPDATE users 
                SET {key} = ?
                WHERE id = ?
""", (value,id))
    base.commit()
    
def setServerValue(id: int, key: str, value: str):
    serverCheck(id)
    cur.execute(f"""
                UPDATE servers 
                SET {key} = ?
                WHERE id = ?
""", (value,id))
    base.commit()



def addValues(table: str, names:list, values: list):
    additiven = str(names)[1:-1]
    additive = str(values)[1:-1]
    cur.execute(f"""
                INSERT INTO {table} ({additiven})
                VALUES ({additive})
""")
    base.commit()


    
def getLenOfRecordsTable(table: str, key:str, value:int):
    result = cur.execute(f'SELECT * FROM {table} WHERE {key} = ?', (value,)).fetchall()
    print(result)
    if result:
        return len(result)
    else:
        return 0
    
def getAllTableValues(table: str, key:str, value:int):
    result = cur.execute(f"SELECT * FROM {table} WHERE {key} = ?", (value,)).fetchall()
    if result:
        return result
    else:
        return None
    
def getTableValues(table: str, key:str, value:int, val:str):
    result = cur.execute(f"SELECT {val} FROM {table} WHERE {key} = ?", (value,)).fetchall()
    if result:
        return result
    else:
        return None

def getTableValue(table: str, key:str, value:int):
    result = cur.execute(f"SELECT * FROM {table} WHERE {key} = ?", (value,)).fetchone()
    if result:
        return result[0]
    else:
        return None
    
def getTableValuesByTwoKeys(table:str,key1:str,value1:int, key2:str,value2:int):
    result = cur.execute(f"SELECT * FROM {table} WHERE {key1} = ? AND {key2} = ?", (value1, value2,)).fetchone()
    
    if result:
        return result
    else:
        return None
    
# def getTableValuesByTwoKeysINTSTR(table:str,key1:str,value1:int, key2:str,value2:str):
#     result = cur.execute(f"SELECT * FROM {table} WHERE {key1} = ? AND {key2} = '?'", (value1,value2,)).fetchone()
#     if result:
#         return result
#     else:
#         return None


def getAllTableValuesByOneKey(table:str,key1:str,value1:int):
    result = cur.execute(f"SELECT * FROM {table} WHERE {key1} = ?", (value1,)).fetchall()
    if result:
        return result
    else:
        return None

def delRowFromTableByKey(table:str, key:str, value:int):
    try:
        cur.execute(f"DELETE FROM {table} WHERE {key}=?", (value,))
        base.commit()
        return 0
    except:

        return -1
    
def delRowFromTableByTwoKeys(table:str, key1:str, value1:int, key2:str, value2:int):
    try:
        cur.execute(f"DELETE FROM {table} WHERE {key1}=? AND {key2}=?", (value1,value2,))
        base.commit()
        return 0
    except:

        return -1
    



# Getters
def getUser(id: int):
    return cur.execute(f"SELECT * FROM users WHERE id = ?", (id,)).fetchone()

def getServer(id: int):
    return cur.execute(f"SELECT * FROM servers WHERE id = ?", (id,)).fetchone()

# Getters (keys)
def getUserKey(id: int, key: str):
    return cur.execute(f"SELECT {key} FROM users WHERE id = ?", (id,)).fetchone()[0]

def getServerKey(id: int, key: str):
    res=  cur.execute(f"SELECT {key} FROM servers WHERE id = ?", (id,)).fetchone()
    if res:
        return res[0]
    else:
        return None

def addColumnDB(table: str, column: str, default_value=None): # Adds column to DB
    try:
        if default_value != None:
            cur.execute(f"SELECT {column} FROM {table} DEFAULT {default_value}")
        else:
            cur.execute(f"SELECT {column} FROM {table}")
    except sqlite3.OperationalError:
        if default_value != None:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT DEFAULT {default_value}")
        else:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")



        


def initDataBaseCheck(): # Checks DB integrity before starting
    cur.execute("CREATE TABLE IF NOT EXISTS servers(id)")
    cur.execute("CREATE TABLE IF NOT EXISTS users(id)")

    cur.execute("CREATE TABLE IF NOT EXISTS celebrations(id INTEGER PRIMARY KEY AUTOINCREMENT)")
    cur.execute("CREATE TABLE IF NOT EXISTS celebration_templates(id INTEGER PRIMARY KEY AUTOINCREMENT)")

    
    cur.execute("CREATE TABLE IF NOT EXISTS writes(id INTEGER PRIMARY KEY AUTOINCREMENT)")


    cur.execute("CREATE TABLE IF NOT EXISTS msgs_writes(id INTEGER PRIMARY KEY AUTOINCREMENT)")
    cur.execute("CREATE TABLE IF NOT EXISTS del_channels(id INTEGER PRIMARY KEY AUTOINCREMENT)")


    cur.execute("CREATE TABLE IF NOT EXISTS access_levels(id INTEGER PRIMARY KEY AUTOINCREMENT)")

    cur.execute("CREATE TABLE IF NOT EXISTS texts(id INTEGER PRIMARY KEY AUTOINCREMENT)")

    # Server | DataBaseServer
    # id included by default upper

    addColumnDB('servers', 'birthday_roleid')
    addColumnDB('servers', 'birthday_channelid')
    addColumnDB('servers', 'last_celebrationindex')

    # User | DataBaseUser
    # id included by default upper
    # addColumnDB('users', 'birth_date')


    #

    addColumnDB('writes', 'server_id')
    addColumnDB('writes', 'date')
    

    addColumnDB('msgs_writes', 'server_id')
    addColumnDB('msgs_writes', 'chan_id')
    addColumnDB('msgs_writes', 'msg_id')
    addColumnDB('msgs_writes', 'when_unix')

    addColumnDB('del_channels', 'server_id')
    addColumnDB('del_channels', 'chan_id')
    addColumnDB('del_channels', 'unix')
    
    # Celebrations | DataBaseCelebrations

    addColumnDB('celebrations', 'user_id')
    addColumnDB('celebrations', 'server_id')
    addColumnDB('celebrations', 'date')

    # CelebrationTemplates | DatabaseTemplates

    addColumnDB('celebration_templates', 'server_id')
    addColumnDB('celebration_templates', 'internal_id')
    addColumnDB('celebration_templates', 'title')
    addColumnDB('celebration_templates', 'description')
    addColumnDB('celebration_templates', 'color')
    addColumnDB('celebration_templates', 'image')

    #

    addColumnDB('texts', 'guild_id')
    addColumnDB('texts', 'text')


    base.commit()


def DataBaseCheck(i: discord.Interaction): # Checks both server and user with Interaction reference
    serverid = i.guild.id
    serverCheck(serverid)
    userid = i.user.id
    userCheck(userid)

# 03.08.2023
def makeList(value: str) -> list[str]:
    array = []
    if value == None:
        return array
    value = value.split(',')
    for i in value:
        array.append(i)
    return array    

def makeText(list:list[str]) -> str:
    result = ""
    for i in list:
        if result == "":
            result = i
        else:
            result = result + "," + i

def searchList(list:list[str], value:str):
    value = str(value)
    if list == None:
        return -1
    for ind,i in enumerate(list):
        if str(i) == value:
            return ind
    return -1

def appendText(text:str, value:str):
    result = ""
    if text == None or text == "":
        result = str(value)
    else:
        result = str(text) + "," + str(value)
    return result

def popText(text:str, value:str) -> str:
    textList = makeList(text)
    search = searchList(textList, value)
    if search != -1:
        textList.pop(search)
        return makeText(textList)
    else:
        return text