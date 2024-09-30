# Wi-Fi Point System
This tool is a Python3 script designed to reward users who connect to a Wi-Fi network by automatically granting points based on their interactions with the network. The system detects and registers connected devices, associating each device with the corresponding player and updating their score according to their activity on the network.

**IMPORTANT NOTE** ➜ This tool is designed for Movistar routers that feature a Network Map section.

![image](https://github.com/user-attachments/assets/913f2f45-d851-4ddd-9752-d83180afcfe7)

# Requerements
The following components are required for the correct operation of the script:
- Movistar router with the network map.
- [MySQL](https://dev.mysql.com/downloads/) installed.
- [Python3](https://www.python.org/downloads/) installed.

# Installing
First, we will install the repository.

```CMD
git clone https://github.com/h3g0c1v/wifipoints.git
cd wifipoints
```

Now we will have to create the `wifipoints` DB so we will go to our MySQL (`mysql -u root -p`) and create the following DB.

```sql
CREATE DATABASE wifipoints;
USE wifipoints;
```

By default, we will create the user *wifipointsmanager* that will be in charge of managing the `wifipoints` DB, however, we can create it with the name we want but we must make sure to change the values in the `InterfaceConnect.py` script.

```sql
-- Change the user name and password to the one you want --
CREATE USER wifipointsmanager IDENTIFIED BY 'PASSWORD' GRANT ALL ON wifipoints.*;
```

Finally, we will generate the corresponding tables in the `wifipoints` database.

```sql
-- Table where the players will be --
CREATE TABLE players (
	nick VARCHAR(11) NOT NULL PRIMARY KEY,
	name VARCHAR(11),
	mac VARCHAR(17) NOT NULL
);
```
```sql
-- Table storing the players' points --
CREATE TABLE players_points (
	nick VARCHAR(11) NOT NULL PRIMARY KEY,
	name VARCHAR(11),
	points INT(4) NOT NULL,
	FOREIGN KEY (nick) REFERENCES players(nick)
);
```

On the `players` table we must enter the data of the players that will participate. The following are example data:

```sql
-- Inserting sample data --
INSERT INTO players VALUES ('Mama', 'Marta', '11:11:11:11:11:11');
INSERT INTO players VALUES ('Papa', 'Pedro', '22:22:22:22:22:22');
INSERT INTO players VALUES ('Hermano', 'Julio', '33:33:33:33:33:33');
```

These SQL commands are contained in the file `database_structure.sql`.

# Use
The script uses the content of the variables `SESSION_KEY` for the Router password and `MYSQL_PASSWORD` for the MySQL password in order to perform authentications in a more secure way. These variables can be configured in the `management/envSetup.bat` file or configured via terminal on both Windows and Linux:

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

With the variables configured, we will run the script with *Python3*.

```CMD
python3 InterfaceConnect.py
```

If this is the first time you run the script, the result will be as follows. Afterwards, you can run the script whenever you want to check if someone has won a point.

![image](https://github.com/user-attachments/assets/8eef03a9-053a-4f08-926d-5a0bfb8ed1a8)

If no one has connected after the last execution of the script, the following output will appear:

![image](https://github.com/user-attachments/assets/18fe4c1f-6721-414e-9252-4b74847a8ca9)

If someone has earned points, the output will change as follows:

![image](https://github.com/user-attachments/assets/3048b2cb-6417-4d09-8495-4ff6d356cdbb)

# Ranking
To see the points ranking, we must run the script `leaderboard\GenerateLeaderBoard.py` to generate the file `leaderboard.html` in which we will visualize the ranking:

![image](https://github.com/user-attachments/assets/29a4d990-f009-4275-909f-379815be6305)

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
