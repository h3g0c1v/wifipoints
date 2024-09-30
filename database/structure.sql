-- DB --
CREATE DATABASE wifipoints;
USE wifipoints;

-- Change the user name and password to the one you want --
CREATE USER wifipointsmanager IDENTIFIED BY 'PASSWORD' GRANT ALL ON wifipoints.*;

-- Table where the players will be --
CREATE TABLE players (
	nick VARCHAR(11) NOT NULL PRIMARY KEY,
	name VARCHAR(11),
	mac VARCHAR(17) NOT NULL
);

-- Table storing the players' points --
CREATE TABLE players_points (
	nick VARCHAR(11) NOT NULL PRIMARY KEY,
	name VARCHAR(11),
	points INT(4) NOT NULL,
	FOREIGN KEY (nick) REFERENCES players(nick)
);

-- Inserting sample data --
INSERT INTO players VALUES ('Mom', 'Mary', '11:11:11:11:11:11');
INSERT INTO players VALUES ('Dad', 'James', '22:22:22:22:22:22');
INSERT INTO players VALUES ('Brother', 'Michael', '33:33:33:33:33:33');
