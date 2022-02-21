import server

db = server.db

class Course(db.Model):
    __tablename__ = 'course'
    code = db.Column(
        db.Character(8),
        primary_key=True
    )
    description = db.Column(
        db.String(200),
        index=False,
        unique=True,
        nullable=False
    )
    prereq = db.Column(
        db.Character(8),
        index=True,
        unique=True,
        nullable=True
    )
    xlist = db.Column(
        db.Character(8),
        index=True,
        unique=True,
        nullable=True
    )

    def __repr__(self):
        return '<Course {}>'.format(self.course)