import sqlite3
import server
from flask_sqlalchemy import SQLAlchemy

# processed is a list of match_id and match_text
def doQueries(processed):
    db = SQLAlchemy(server.app)
    print(processed)
    if processed:
        print()
    print(db.Course.query.all())
    return 'placeholder return'