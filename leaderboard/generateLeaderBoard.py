import mysql.connector
import os

if (not os.getenv("MYSQL_PASSWORD")):
    print("[!] Please set the MYSQL_PASSWORD environment variable")
    exit(1)

# Conectar a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="wifipointsmanager",
    password=os.getenv("MYSQL_PASSWORD"),
    database="wifipoints"
)

cursor = db.cursor()

# Obtener los datos de la tabla players_points
query = "SELECT nick FROM players_points ORDER BY points DESC"
cursor.execute(query)
result = cursor.fetchall()

# Crear el archivo HTML
with open("leaderboard.html", "w") as file:
    file.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wi-Fi Points Ranking</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f7f5f2;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            flex-direction: column;
        }

        .ranking-container {
            background-color: #fefefe;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 600px;
            padding: 20px;
        }

        h1 {
            text-align: center;
            color: #666;
            font-size: 2.5em;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        table th, table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        table th {
            background-color: #b0e0e6; /* Pastel light blue */
            color: #fff;
        }

        table tr:nth-child(even) {
            background-color: #f0f8ff; /* Pastel blue */
        }

        table tr:nth-child(odd) {
            background-color: #faf0e6; /* Pastel light beige */
        }

        .position {
            text-align: center;
            background-color: #f9c6c9; /* Pastel pink */
            color: #fff;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: inline-block;
            line-height: 30px;
        }
    </style>
</head>
<body>
    <div class="ranking-container">
        <h1>Wi-Fi Points Leaderboard</h1>
        <table>
            <thead>
                <tr>
                    <th>Position</th>
                    <th>Nickname</th>
                </tr>
            </thead>
            <tbody>
""")

    # Escribir los datos de los jugadores en el HTML
    position = 1
    for row in result:
        nick = row[0]
        file.write(f"""
        <tr>
            <td><span class="position">{position}</span></td>
            <td>{nick}</td>
        </tr>
        """)
        position += 1

    # Cerrar las etiquetas HTML
    file.write("""
            </tbody>
        </table>
    </div>
</body>
</html>
""")

cursor.close()
db.close()

filePath = os.getcwd() + "\leaderboard.html"
print("[i] Visit \"" + filePath + "\" to see the leaderboard panel")
