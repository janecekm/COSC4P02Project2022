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

class Offering(db.Model):
    __tablename__ = 'offering'
    code = db.Column(
        db.String(8),
        primary_key=True
    )

    frmt = db.Column(
        db.String(8),
        index=True,
        unique=True,
        nullable=True
    )