import sqlite3
from flask import Flask, render_template, request, json
from flask_sqlalchemy import SQLAlchemy
import botNLP as bN
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/buchatbot.db'
db = SQLAlchemy(app)
# db = sqlite3.connect('sqlite:///database/buchatbot.db')

class Course(db.Model):
    __tablename__ = 'course'
    code = db.Column(
        db.String(8),
        primary_key=True
    )
    description = db.Column(
        db.String(200),
        index=False,
        unique=True,
        nullable=False
    )
    prereq = db.Column(
        db.String(100),
        index=True,
        unique=True,
        nullable=True
    )
    xlist = db.Column(
        db.String(8),
        index=True,
        unique=True,
        nullable=True
    )

    def __repr__(self):
        return '\nCode '+self.code+'\n Description '+self.description+'\n Prereq'+self.prereq+'\n Crosslist'+self.xlist

db.create_all()  

@app.route("/brock", methods = ['POST'])
def front():
    print(json.loads(request.data)['message'])
    return bN.processQ(json.loads(request.data)['message'])
@app.route("/",methods=['GET'])
def splashart():
    return render_template("splash.html")

# port=5000 OR host='0.0.0.0'
if __name__ == "__main__":
    if "PORT" in os.environ:
        connectingport = os.environ.get("PORT")
    else:
        connectingport = 5000
    app.run(host="0.0.0.0", port=connectingport)