import sqlite3
import server
#import models
from flask_sqlalchemy import SQLAlchemy

# processed is a list of match_id and match_text
def doQueries(processed):
    db = server.db
    # print(processed)
    if 'course code' and ('prereqs' or 'description') in processed:
        print(processed.get('course code'))
        temp = server.Course.query.filter_by(code='COSC4P03').first()
        print(temp.description)
        # print(server.Course.query.filter_by(code=processed.get('course code')).first())
    # print(server.Course.query.all())
    return 'placeholder return'