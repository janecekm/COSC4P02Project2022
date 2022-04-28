DROP TABLE IF EXISTS course;
CREATE TABLE course (
	code CHAR(8) PRIMARY KEY,
	title VARCHAR(40),
	format VARCHAR(40),
	description VARCHAR(200),
	prereq VARCHAR(100),
	xlist CHAR(8),
	restriction VARCHAR(40)
);

DROP TABLE IF EXISTS offering;
CREATE TABLE offering (
	code CHAR(8),
	format VARCHAR(8),
	formatNum VARCHAR(4),
	duration CHAR(2),
	section CHAR(2),
	days CHAR(7),
	time TIME,
	location CHAR(20),
	instructor CHAR(30),
	PRIMARY KEY(code, days, time, location)
);

DROP TABLE IF EXISTS exam;
CREATE TABLE exam (
	code CHAR(8),
	time TIME,
	day VARCHAR(14),
	dayNum CHAR(2),
	month VARCHAR(14),
	section CHAR(2),
	location CHAR(10)
);

DROP TABLE IF EXISTS building;
CREATE TABLE building (
	code VARCHAR(10),
	name VARCHAR(30),
	PRIMARY KEY(code)
);

DROP TABLE IF EXISTS program;
CREATE TABLE program (
	program VARCHAR(20),
	link VARCHAR(60),
	PRIMARY KEY(program)
);

-- INSERT INTO course VALUES ('COSC4P03', 'this is a description', 'COSC3P03', 'COSC3P03');