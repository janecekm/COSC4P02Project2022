import json
import sqlite3

def building_codes():
    filename = 'buildingCodes.txt'
    with open(filename, 'r') as f:
        contents = f.read()
    codes = json.loads(contents)
    return codes

def populate_db_building_codes(db='buchatbot.db'):
    connection = sqlite3.connect(db)
    with connection:
        codes = building_codes()
        cursor = connection.cursor()
        flag = True
        for c in codes:
            codes[c] = codes[c].replace('\'', '')
            if not flag:
                print(c)
                print(codes[c])
                cursor.execute('INSERT INTO course VALUES ('+c+', '+codes[c]+')')
            else:
                flag=False

populate_db_building_codes()