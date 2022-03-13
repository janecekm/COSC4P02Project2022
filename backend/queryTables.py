import sqlite3
import server
#import models
from flask_sqlalchemy import SQLAlchemy

# keywords is a dictionary of match_id and match_text
def doQueries(keywords):
    db = server.db
    # print(keywords)
    if 'course code' and ('prereqs' or 'description') in keywords:
        print(keywords.get('course code'))
        filterCourseInputs(keywords)
        # temp = server.Course.query.filter_by(code='COSC4P03').first()
        # print(temp.description)
        print(server.Course.query.filter_by(code=keywords.get('course code')).first())
    # print(server.Course.query.all())
    return 'placeholder return'

# filter to match database formatting
def filterCourseInputs(keywords):
    temp = keywords.get('course code').text
    temp = temp.upper()
    print("filtered input: "+temp)
    keywords['course code'] = temp
    return None