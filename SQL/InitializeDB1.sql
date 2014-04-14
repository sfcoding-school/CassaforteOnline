DROP DATABASE IF EXISTS server1;
CREATE DATABASE IF NOT EXISTS server1;

USE server1;

CREATE TABLE slice(
	id INTEGER UNSIGNED,
    slice_n INTEGER UNSIGNED NOT NULL,
    uid VARCHAR(100) UNIQUE,
    PRIMARY KEY(id)
);

/*
INSERT INTO slice values(1,1,'0010');
INSERT INTO slice values(2,2,'0011');
INSERT INTO slice values(3,3,'0012');
*/
DROP DATABASE IF EXISTS server2;
CREATE DATABASE IF NOT EXISTS server2;

USE server2;

CREATE TABLE slice(
	id INTEGER UNSIGNED,
    slice_n INTEGER UNSIGNED NOT NULL,
    uid VARCHAR(100) UNIQUE,
    PRIMARY KEY(id)
);
/*
INSERT INTO slice values(1,2,'0020');
INSERT INTO slice values(2,3,'0021');
INSERT INTO slice values(3,1,'0022');
*/
DROP DATABASE IF EXISTS server3;
CREATE DATABASE IF NOT EXISTS server3;

USE server3;

CREATE TABLE slice(
	id INTEGER UNSIGNED,
    slice_n INTEGER UNSIGNED NOT NULL,
    uid VARCHAR(100) UNIQUE,
    PRIMARY KEY(id)
);
/*
INSERT INTO slice values(1,3,'0030');
INSERT INTO slice values(2,1,'0031');
INSERT INTO slice values(3,2,'0032');
*/
