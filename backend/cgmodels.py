from server import db

'''
	sport VARCHAR(25) PRIMARY KEY,
	month VARCHAR(12),
    date CHAR(2)
	day CHAR(7),
	year VARCHAR(200),
	time TIME,
	gender VARCHAR(10),
	event VARCHAR(40)
    stage VARCHAR(20)
    round VARCHAR(20)
    venue VARCHAR(40)

    Some things might be incorrectly labelled as INDEX/NULLABLE, used best judgement
'''
class Schedule(db.Model):
    __tablename__ = 'schedule'
    sport = db.Column(
        db.String(8),
        primary_key=True,
        index = True,
        unique = False,
        nullable = False
    )

    month = db.Column(
        db.String(8),
        index=True,
        unique=False,
        nullable=True
    )

    date = db.Column(
        db.String(8),
        index=True,
        unique=False,
        nullable=True
    )

    day = db.Column (
        db.String(2),
        index = True,
        unique = False,
        nullable = True
    )

    year = db.Column (
        db.String(2),
        index = True,
        unique = False,
        nullable = True
    )

    time = db.Column(
        db.String(7),
        primary_key=True,
        index = False,
        unique = False,
        nullable = False
    )

    gender = db.Column (
        #er, does Python have a TIME type?
        #for now accomodates 2 times and a space in frmt 00:00 11:11
        db.String(11),
        primary_key=True,
        index = False,
        unique = False,
        nullable = False
    )

    event = db.Column (
        db.String(20),
        primary_key=True,
        index = True,
        unique = False,
        nullable = True
    )

    stage = db.Column(
        db.String(30),
        index = True,
        unique = False,
        nullable = True
    )

    round = db.Column(
        db.String(30),
        index = True,
        unique = False,
        nullable = True
    )

    venue = db.Column(
        db.String(30),
        index = True,
        unique = False,
        nullable = True
    )

    def __repr__(self):
        return '\nSport '+self.sport+'\n Month '+self.month+'\n Date '+self.date+'\n Day '+self.day+'\n Year'+self.year+'\n Time'+self.time+'\n Gender'+self.gender+'\n Event'+self.event+'\n Stage'+self.stage+'\n Round'+self.round+'\n Venue'+self.venue
