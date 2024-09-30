# Wi-Fi point system
This tool is a Python3 script designed to reward users who connect to a Wi-Fi network by automatically granting points based on their interactions with the network. The system detects and registers connected devices, associating each device with the corresponding player and updating their score according to their activity on the network.

**IMPORTANT NOTE** ➜ This tool is designed for Movistar routers that feature a Network Map section.

![image](https://github.com/user-attachments/assets/913f2f45-d851-4ddd-9752-d83180afcfe7)

# Requerements
The following components are required for the correct operation of the script:
- Movistar router with the network map.
- [MySQL](https://dev.mysql.com/downloads/) installed.
- [Python3](https://www.python.org/downloads/) installed.

# Installing
Primeramente, instalaremos el repositorio 

```CMD
git clone https://github.com/h3g0c1v/wifipoints.git
cd wifipoints
```

Ahora tendremos que crear la BBDD `wifipoints` por lo que nos iremos a nuestro MySQL (`mysql -u root -p`) y crearemos la siguiente BD.

```sql
CREATE DATABASE wifipoints;
USE wifipoints;
```

Por defecto, crearemos el usuario *wifipointsmanager* que se encargará de administrar la BD `wifipoints`, sin embargo, podremos crearlo con el nombre que deseemos pero nos debemos de asegurar de cambiar los valores en el script `InterfaceConnect.py`.

```sql
-- Cambiar el nombre de usuario y contraseña al que queramos --
CREATE USER wifipointsmanager IDENTIFIED BY 'CONTRASEÑA' GRANT ALL ON wifipoints.*;
```

Por último generaremos las tablas correspondientes en la BD `wifipoints`.

```sql
-- Tabla donde estarán los jugadores --
CREATE TABLE players (
	nick VARCHAR(11) NOT NULL PRIMARY KEY,
    name VARCHAR(11),
    mac VARCHAR(17) NOT NULL
);
```
```sql
-- Tabla que almancena los puntos de los jugadores --
CREATE TABLE players_points (
	nick VARCHAR(11) NOT NULL PRIMARY KEY,
	name VARCHAR(11),
	points INT(4) NOT NULL,
    FOREIGN KEY (nick) REFERENCES players(nick)
);
```

Sobre la tabla `players` deberemos de introducir los datos de los jugadores que van a participar. Los siguientes son datos de ejemplo:

```sql
-- Insertando datos de ejemplo --
INSERT INTO players VALUES ('Mama', 'Marta', '11:11:11:11:11:11');
INSERT INTO players VALUES ('Papa', 'Pedro', '22:22:22:22:22:22');
INSERT INTO players VALUES ('Hermano', 'Julio', '33:33:33:33:33:33');
```

# Uso
El script utiliza el contenido de las variables `SESSION_KEY` para la contraseña del Router y `MYSQL_PASSWORD` para la contraseña de MySQL con el fín de poder efectuar autenticaciones de manera más segura. Podremos configurar estas variables en el fichero `management/envSetup.bat` o configurarlas por terminal tanto en Windows como en Linux:

**WINDOWS**
```CMD
set SESSION_KEY=myRouterPassword
set MYSQL_PASSWORD=mysqlPassword
```

**LINUX**
```bash
export SESSION_KEY="myRouterPassword"
export MYSQL_PASSWORD="mysqlPassword"
```

Con las variables configuradas, ejecutaremos el script con *Python3*.

```CMD
python3 InterfaceConnect.py
```

# Clasificación
Para ver la clasificación de puntos, deberemos de ejecutar el script `leaderboard\generateLeaderBoard.py` para generar el fichero `leaderboard.html` en el cual visualizaremos la clasificación.

![image](https://github.com/user-attachments/assets/48c0e6b9-6a09-493d-9fee-d5fa2765f4ca)


## Key Components:
The key components of this tool are:
- **Device Detection**: Through an authentication process, it accesses the network map where connected devices are listed, identified by their MAC addresses.
- **Device-to-Player Association**: The connected device is associated with a player by it's MAC address, previously registered in the players database. Players are identified by a nickname and a name.
- **Point System**: Each time the player's device reconnects, points are awarded to the corresponding player. These points are recorded in the database table called *players_points*.
- **Database Management**: A MySQL database is used to store information about players and their scores. The main tables are:
  - `players`: Stores information about players, such as their nickname, name, and the device's MAC address.
  - `players_points`: Records the points accumulated by each player.

## Script Functionality
The following steps outline the script's process:
1. **Authentication** with the router to access the network map.
2. **Device Comparison** between sessions to identify newly connected devices and update scores.
3. **Data Backup**, where activity files are automatically compressed.
4. **Security and Credential Management**: To access the router or database, the system uses environment variables for credential management.

I hope it helps you <3
