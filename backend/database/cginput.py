import json
import sqlite3

def loadFile(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    codes = json.loads(contents)
    return codes

def schedule_populate(db='cgchatbot.db'):
    with open('./cleandata/schedule.txt', 'r') as f:
            codes = f.readlines()
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        for line in codes:
            JSONDecodedRow = json.loads(line)
            sport = JSONDecodedRow.get('sports') or ""
            month = JSONDecodedRow.get('month') or ""
            date = JSONDecodedRow.get('date') or ""
            day = JSONDecodedRow.get('day') or ""
            year = JSONDecodedRow.get('year') or ""
            time = JSONDecodedRow.get('time') or ""
            gender = JSONDecodedRow.get('gender') or ""
            event = JSONDecodedRow.get('specific-event') or ""
            event = event.replace('\'', '`')
            stage = JSONDecodedRow.get('stage') or ""
            stage = stage.replace('\'', '`')
            round = JSONDecodedRow.get('game') or ""
            round = round.replace('\'', '`')
            venue = JSONDecodedRow.get('venue') or ""
            venue = venue.replace('\'', '`')

            cursor.execute('INSERT OR IGNORE INTO schedule(sport, month, date, day, year, time, gender, event, stage, round, venue) VALUES (\''+sport+'\', \''+month+'\', \''+date+'\', \''+day+'\', \''+year+'\', \''+time+'\', \''+gender+'\', \''+event+'\', \''+stage+'\', \''+round+'\', \''+venue+'\')')
        
schedule_populate()