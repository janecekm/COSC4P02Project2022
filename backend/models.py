from server import db

class Course(db.Model):
    # __bind_key__ = 'brock'
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
        unique=False,
        nullable=True
    )
    xlist = db.Column(
        db.String(8),
        index=True,
        unique=False,
        nullable=True
    )

    title = db.Column(
        db.String(40),
        index=True,
        unique=True,
        nullable=True
    )

    format = db.Column(
        db.String(40),
        index=True,
        unique=False,
        nullable=True
    )

    restriction = db.Column(
        db.String(40),
        index=True,
        unique=False,
        nullable=True
    )

    def __repr__(self):
        return '\nCode '+self.code+'\n Description '+self.description+'\n Prereq'+self.prereq+'\n Crosslist'+self.xlist
        # temp = {}
        # temp['code'] = self.code
        # temp['description'] = self.description
        # temp['prereq'] = self.prereq
        # temp['xlist'] = self.xlist
        # return temp

'''
	code CHAR(8),
	frmt VARCHAR(8),
	duration CHAR(2),
	section CHAR(2),
	days CHAR(7),
	time TIME,
	location CHAR(20),
	instructor CHAR(30)

    Some things might be incorrectly labelled as INDEX/NULLABLE, used best judgement
'''
class Offering(db.Model):
    __tablename__ = 'offering'
    code = db.Column(
        db.String(8),
        primary_key=True,
        index = True,
        unique = False,
        nullable = False
    )

    format = db.Column(
        db.String(8),
        index=True,
        unique=False,
        nullable=True
    )

    formatNum = db.Column(
        db.String(8),
        index=True,
        unique=False,
        nullable=True
    )

    duration = db.Column (
        db.String(2),
        index = True,
        unique = False,
        nullable = True
    )

    section = db.Column (
        db.String(2),
        index = True,
        unique = False,
        nullable = True
    )

    days = db.Column(
        db.String(7),
        primary_key=True,
        index = False,
        unique = False,
        nullable = False
    )

    time = db.Column (
        #er, does Python have a TIME type?
        #for now accomodates 2 times and a space in frmt 00:00 11:11
        db.String(11),
        primary_key=True,
        index = False,
        unique = False,
        nullable = False
    )

    location = db.Column (
        db.String(20),
        primary_key=True,
        index = True,
        unique = False,
        nullable = True
    )

    instructor = db.Column(
        db.String(30),
        index = True,
        unique = False,
        nullable = True
    )

    def __repr__(self):
        return '\nCode '+self.code+'\n Format '+self.format+'\n FormatNum '+self.formatNum+'\n Duration'+self.duration+'\n Section'+self.section+'\n days'+self.days+'\n time'+self.time+'\n location'+self.location+'\n Instructor'+self.instructor


'''
{'courseCode': 'ACTG 4P42', 'time': '19:00-22:00', 'day': 'Friday', 'dayNumber': '22', 'month': 'April', 'sec': '1', 'location': 'STH217'}
DROP TABLE IF EXISTS exam;
CREATE TABLE exam (
	code CHAR(8),
	time TIME,
	day VARCHAR(14),
	dayNum INT,
	month VARCHAR(14),
	sec INT,
	location CHAR(10)
);
'''

class Exam(db.Model):
    __tablename__ = 'exam'
    code = db.Column(
        db.String(8),
        primary_key = True,
        index = True,
        unique = False,
        nullable = False
    )

    time = db.Column (
        #er, does Python have a TIME type?
        #for now accomodates 2 times and a space in frmt 00:00 11:11
        db.String(11),
        index = False,
        unique = False,
        nullable = False
    )

    day = db.Column(
        db.String(14),
        index = False,
        unique = False,
        nullable = False
    )

    dayNum = db.Column(
        db.String(2),
        index = False,
        unique = False,
        nullable = False
    )

    month = db.Column(
        db.String(14),
        index = False,
        unique = False,
        nullable = False

    )

    section = db.Column (
        db.String(2),
        index = True,
        unique = False,
        nullable = True
    )

    location = db.Column (
        db.String(10),
        index = True,
        unique = False,
        nullable = True
    )

    def __repr__(self):
        return '\nCode '+self.code+'\n Section'+self.section+'\n day'+self.day+'\n time'+self.time+'\n location'+self.location

class Building(db.Model):
    __tablename__ = 'building'
    code = db.Column(
        db.String(10),
        primary_key = True,
        index = True,
        unique = True,
        nullable = False
    )

    name = db.Column (
        db.String(30),
        index = False,
        unique = True,
        nullable = False
    )

    def __repr__(self):
        return '\nCode '+self.code+'\n Name'+self.name

class Program(db.Model):
    __tablename__ = 'program'
    program = db.Column(
        db.String(30),
        primary_key = True,
        index = True,
        unique = True,
        nullable = False
    )

    link = db.Column (
        db.String(60),
        index = False,
        unique = True,
        nullable = False
    )

    def __repr__(self):
        return '\nProgram '+self.program+'\n Link '+self.link

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
    __bind_key__ = 'canada'
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
