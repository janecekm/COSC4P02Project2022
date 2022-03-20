from server import db

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
        primary_key=True
    )

    frmt = db.Column(
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
        index = False,
        unique = False,
        nullable = True
    )

    time = db.Column (
        #er, does Python have a TIME type?
        #for now accomodates 2 times and a space in frmt 00:00 11:11
        db.String(11),
        index = False,
        unique = False,
        nullable = True
    )

    location = db.Column (
        db.String(20),
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
        return '\nCode '+self.code+'\n Format '+self.frmt+'\n Duration'+self.duration+'\n Section'+self.section+'\n days'+self.days+'\n time'+self.time+'\n location'+self.location+'\n Instructor'+self.instructor