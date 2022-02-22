import json
import sqlite3

def loadFile(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    codes = json.loads(contents)
    return codes

def populate_db_building_codes(db='buchatbot.db'):
    connection = sqlite3.connect(db)
    with connection:
        codes = loadFile('buildingCodes.txt')
        cursor = connection.cursor()
        flag = True
        for c in codes:
            codes[c] = codes[c].replace('\'', '`')
            if not flag:
                print(c)
                print(codes[c])
                cursor.execute('INSERT INTO course(code, description) VALUES (\''+c+'\', \''+codes[c]+'\')')
            else:
                flag=False

def course_table_populate(db='buchatbot.db'):
    connection = sqlite3.connect(db)
    with connection:
        codes = loadFile('courseinfo.txt')
        cursor = connection.cursor()
        for c in codes:
            codes[c]['description'] = codes[c]['description'].replace('\'', '`')
            # json.loads(codes[c])
            # print(codes[c].get('prereq'))
            if 'prereq' in codes[c]:
                p = codes[c]['prereq']
            else:
                p = ''
            if 'xlist' in codes[c]:
                x = codes[c]['xlist']
            else:
                x = ''
            cursor.execute('INSERT INTO course(code, description, prereq, xlist) VALUES (\''+c+'\', \''+codes[c]['description']+'\', \''+p+'\', \''+x+'\')')

# populate_db_building_codes()
course_table_populate()