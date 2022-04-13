import json
import sqlite3

def loadFile(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    codes = json.loads(contents)
    return codes

def populate_db_building_codes(db='buchatbot.db'):
    with open('./cleandata/buildingCodesClean.txt', 'r') as f:
            codes = f.readlines()
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        for line in codes:
            JSONDecodedRow = json.loads(line)
            code = JSONDecodedRow.get('buildingCode') or ""
            name = JSONDecodedRow.get('title') or ""
            name = name.replace('\'', '`')

            cursor.execute('INSERT OR IGNORE INTO building(code, name) VALUES (\''+code+'\', \''+name+'\')')
        
    # connection = sqlite3.connect(db)
    # with connection:
    #     codes = loadFile('buildingCodes.txt')
    #     cursor = connection.cursor()
    #     flag = True
    #     for c in codes:
    #         codes[c] = codes[c].replace('\'', '`')
    #         if not flag:
    #             print(c)
    #             print(codes[c])
    #             cursor.execute('INSERT INTO course(code, description) VALUES (\''+c+'\', \''+codes[c]+'\')')
    #         else:
    #             flag=False

def course_populate(db='buchatbot.db'):
    with open('./cleandata/course.txt', 'r') as f:
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

#{'courseCode': 'ACTG 4P42', 'time': '19:00-22:00', 'day': 'Friday', 'dayNumber': '22', 'month': 'April', 'sec': '1', 'location': 'STH217'}
'''
CREATE TABLE exam (
	code CHAR(8),
	time TIME,
	day VARCHAR(14),
	dayNum INT,
	month VARCHAR(14),
	sec INT,
	location CHAR(10)
'''
def exam_populate(db='buchatbot.db'):
    with open('./cleandata/exams.txt','r') as f:
        codes = f.readlines()
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        for line in codes:
            JSONDecodedRow = json.loads(line)
            code = JSONDecodedRow.get('code') or ""
            time = JSONDecodedRow.get('time') or ""
            day = JSONDecodedRow.get('day') or ""
            dayNumber = JSONDecodedRow.get('dayNumber') or ""
            month = JSONDecodedRow.get('month') or ""
            section = JSONDecodedRow.get('sec') or ""
            location = JSONDecodedRow.get('location') or ""
            
            cursor.execute('INSERT OR IGNORE INTO exam(code, time, day, dayNum, month, section, location) VALUES (\''+code+'\', \''+time+'\', \''+day+'\', \''+dayNumber+'\', \''+month+'\', \''+section+'\', \''+location+'\')')


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
exam_populate()

