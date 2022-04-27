DROP TABLE IF EXISTS schedule;
CREATE TABLE schedule (
	sport VARCHAR(25),
	month VARCHAR(12),
    date CHAR(2),
	day CHAR(7),
	year VARCHAR(200),
	time TIME,
	gender VARCHAR(10),
	event VARCHAR(40),
    stage VARCHAR(20),
    round VARCHAR(20),
    venue VARCHAR(40),
	PRIMARY KEY(event, stage, round, gender)
);