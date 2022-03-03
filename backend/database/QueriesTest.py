from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import text


#create the engine for SQLAlchemy from the brockdb file
engine = create_engine("sqlite:///buchatbot.db")
Base = automap_base()
Base.prepare(engine, reflect=True)

#Every filter modifier you use has to be imported
from sqlalchemy import or_, and_

#great, automap isn't being the best. It's only recognizing courses. Looks like we have to map the other tables ourselves. 
#Turns out automap gets mad if a table doesn't have a primary key
# https://docs.sqlalchemy.org/en/14/faq/ormconfiguration.html#how-do-i-map-a-table-that-has-no-primary-key
#....the recommended solution is to make up a primary key. Seriously. Just combine fields or something

Course = Base.classes.course

session = Session(engine)

#I actually don't love this way? SQLAlchemy native filter functions might be less awkward
for result in session.query(Course).from_statement(text("SELECT * from Course WHERE code=:code")).params(code='COSC 1P02').all():
    print(result.code, result.description, result.prereq, result.xlist)


#the filters way. Note the chaining - nicer to write, maybe harder to read:
for res in session.query(Course).filter(or_(Course.code == 'COSC 1P02', Course.code == 'COSC 4P02')):
    print(res.code)