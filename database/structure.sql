-- BD --
CREATE DATABASE wifipoints;
USE wifipoints;

-- Cambiar el nombre de usuario y contraseña al que queramos --
CREATE USER wifipointsmanager IDENTIFIED BY 'CONTRASEÑA' GRANT ALL ON wifipoints.*;

-- Tabla donde estarán los jugadores --
CREATE TABLE players (
	nick VARCHAR(11) NOT NULL PRIMARY KEY,
    name VARCHAR(11),
    mac VARCHAR(17) NOT NULL
);

-- Tabla que almancena los puntos de los jugadores --
CREATE TABLE players_points (
	nick VARCHAR(11) NOT NULL PRIMARY KEY,
	name VARCHAR(11),
	points INT(4) NOT NULL,
    FOREIGN KEY (nick) REFERENCES players(nick)
);
