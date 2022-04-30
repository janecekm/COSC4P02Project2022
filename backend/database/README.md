# Database Structure
This application offers two distinct chatbots with separate databases and data pipelines.

## Brock University
The Brock University database contains five tables to answer a number of user queries.

### Course Table
Identified by a course code, this table answers queries relating to course names, descriptions or their restrictions.

### Offering Table
Contains the scheduling information for the current semester. This handles queries such as class times, locations, professors, lab/seminar/tutorial numbers, etc.

### Exam Table
Contains scheduling information for final course examinations.

### Program Table
Contains available programs at Brock and a link to the department page.

### Buildings
To help the user navigate the campus, building codes can be searched for their full name with a link to a campus map.

## Canada Games
Currently primitive to show off the second data pipeline, this includes one table for schedule information.

### Schedule Table
This table has functionality to handle questions regarding sport locations and times.

# Database Infrastructure
Our database uses technologies such as SQLite and Flask-SQLAlchemy. Data is structured, read-only, and requires a low-moderately sized database.

## SQLite
SQLite is a small, fast embedded database that deploys with our application. It also has support for mutiple databases. More documentation can be read [here](https://www.sqlite.org/index.html)

The files that use this are 
- [Brock Database](buchatbot.db)
- [Canada Games Database](cgchatbot.db)

Python scripts were written to input data into the database using a text file generated from web-scraping.

These files are 
- [Brock Input](dbinput.py)
- [Canada Games Input](cginput.py)

We can run these by using the command:

>`python ./dbinput.py`