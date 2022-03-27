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

def course_populate(db='buchatbot.db'):
    with open('course.txt', 'r') as f:
            codes = f.readlines()
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        for line in codes:
            JSONDecodedRow = json.loads(line)
            code = JSONDecodedRow.get('code') or ""
            title = JSONDecodedRow.get('title') or ""
            title = title.replace('\'', '`')
            frmt = JSONDecodedRow.get('frmt') or ""
            frmt = frmt.replace('\'', '`')
            description = JSONDecodedRow.get('description') or ""
            description = description.replace('\'', '`')
            prereq = JSONDecodedRow.get('prereq') or ""
            prereq = prereq.replace('\'', '`')
            xlist = JSONDecodedRow.get('xlist') or ""
            restriction = JSONDecodedRow.get('restriction') or ""
            restriction = restriction.replace('\'', '`')
            
            cursor.execute('INSERT OR IGNORE INTO course(code, title, frmt, description, prereq, xlist, restriction) VALUES (\''+code+'\', \''+title+'\', \''+frmt+'\', \''+description+'\', \''+prereq+'\', \''+xlist+'\', \''+ restriction+'\')')
        # for c in codes:
        #     codes[c]['description'] = codes[c]['description'].replace('\'', '`')
        #     # json.loads(codes[c])
        #     # print(codes[c].get('prereq'))
        #     if 'prereq' in codes[c]:
        #         p = codes[c]['prereq']
        #     else:
        #         p = ''
        #     if 'xlist' in codes[c]:
        #         x = codes[c]['xlist']
        #     else:
        #         x = ''
        #     cursor.execute('INSERT INTO course(code, description, prereq, xlist) VALUES (\''+c+'\', \''+codes[c]['description']+'\', \''+p+'\', \''+x+'\')')


#this appears to execute, unsure how to get rows to display when visiting Flask site though
def offering_populate(db='buchatbot.db'):
    with open('./cleandata/offering.txt', 'r') as f:
            codes = f.readlines()
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        for line in codes:    #didn't want to modify loadFile method to handle this format, so this block decodes each row in timetable.txt one at a time
            #days, time, instructor location, room1, and room2 can all be NoneType and need to be checked. There may be a better way than this. 
            JSONDecodedRow = json.loads(line)
            code = JSONDecodedRow.get('courseCode')
            frmt = JSONDecodedRow.get('type')
            duration = JSONDecodedRow.get('duration')
            sec = JSONDecodedRow.get('sec')
            time = JSONDecodedRow.get('time') or ""
            days = JSONDecodedRow.get('days') or ""
            room1 = JSONDecodedRow.get('room1') or ""
            room2 = JSONDecodedRow.get('room2') or ""
            
            location = JSONDecodedRow.get('loc')
            if location == None:
                location = ''
            else:
                if not room1 == "":
                    # if room2 == None:
                    #     location = location + ' ' + room1
                    if not room2 == "":
                        location = room1 + ' ' + room2

                
            instructor = JSONDecodedRow.get('instructor').replace("\'", "`") or ""
            if instructor == None:
                instructor = ''

            cursor.execute('INSERT OR IGNORE INTO offering(code, frmt, duration, section, days, time, location, instructor) VALUES (\''+code+'\', \''+ frmt+'\', \''+duration+'\', \''+sec+'\', \''+ days+'\', \''+ time+'\', \''+ location+'\', \''+ instructor+'\')')
    

# populate_db_building_codes()

#populate offerings (timetable)
offering_populate()
course_populate()


