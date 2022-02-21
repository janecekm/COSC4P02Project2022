DROP TABLE IF EXISTS course;
CREATE TABLE course (
	code CHAR(8) PRIMARY KEY,
	description VARCHAR(200),
	prereq CHAR(8),
	xlist CHAR(8)
);

DROP TABLE IF EXISTS offering;
CREATE TABLE offering (
	code CHAR(8),
	format VARCHAR(8),
	duration CHAR(2),
	section CHAR(2),
	time TIME,
	location CHAR(10),
	instructor CHAR(30)	
);

DROP TABLE IF EXISTS exam;
CREATE TABLE exam (
	code CHAR(8),
	date DATE,
	time TIME,
	location CHAR(10)
);

INSERT INTO course VALUES ('COSC4P03', 'this is a description', 'COSC3P03', 'COSC3P03');