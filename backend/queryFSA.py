import models
import sqlite3

db = sqlite3.connect('sqlite:///database/buchatbot.db')

# cur = db.cursor()
# cur.execute("SELECT * FROM offering WHERE code=COSC1P03")

# rows = cur.fetchall()

# for row in rows:
#     print(row)

print(models.Offering.query.filter_by(code='COSC1P03').first())