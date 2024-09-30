# Author: h3g0c1v
# This tool is a Python3 script designed to reward users who connect to a Wi-Fi network by automatically granting points based on their interactions with the network.
# The system detects and registers connected devices, associating each device with the corresponding player and updating their score according to their activity on the network.

# Librerías
from bs4 import BeautifulSoup
from datetime import datetime
import requests, signal, re, os
import mysql.connector


# Variables globales
s = requests.Session()
loginUrl = "http://192.168.1.1/login-login.cgi"
netmapUrl = "http://192.168.1.1/networkmap.html"

# Handler - Ctrl + C
def def_handler(sig, frame):
    print("\n[+] Saliendo ...\n")
    exit(1)

signal.signal(signal.SIGINT, def_handler)

# Función para leer el contenido de un archivo
def readFile (filePath):
    # Lee el contenido del archivo y lo devuelve como una lista de líneas.
    with open(filePath, 'r') as file:
        return file.readlines()

# Autenticandonos en el portal del router
def portalConnect():
    print("[i] Autenticandose ...")
    
    autenticationData = {
        "sessionKey": os.getenv("SESSION_KEY"),
        "pass": ""
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        r = s.post(loginUrl, data=autenticationData, headers=headers, verify=False)

        # En caso de que la auth sea exitosa nos responderá con la siguiente respuesta:
        # top.location = /mhs.html
        if "/mhs.html" in r.text:
            print("[+] Autenticación Exitosa!")
            return 0
        else:
            print("[!] Autenticación Fallida!")
            exit(1)
    except Exception as e:
        print(f"[!] ERROR: {e}")
        exit(1)

# Obteniendo el mapa de red sobre networkmap.html
def getNetworkMap():
    print("[i] Obteniendo el mapa de red ...")
    
    r = s.get(netmapUrl)
    return (r)

# Filtramos el resultado obtenido en el mapa de red
def parseDevices(r, filePath):
    infoParsed = BeautifulSoup(r.text, 'html.parser') # Usamos BeautifulSoup para parsear el HTML
    devices = infoParsed.find_all('div', class_='cssTdVertical') # Encontramos todos los span con la clase 'imgLink black2' (es donde se encuenta la info de cada device)

    nameList = [] #
    ipList = []   # Definimos las listas para almacenar nombre, IP y MAC del device
    macList = []  #
    
    # Recorremos cada resultado de la información de cada device para ir añadiendo los nombres, IP y MAC de cada device en las listas correspondientes
    for device in devices:
        # Extraemos el contenido de la etiqueta <img> y el onclick donde están nombre, IP y MAC
        imgTag = device.find('img', class_='imgLink')
        
        if imgTag and 'onclick' in imgTag.attrs:
            # Usamos regex para extraer el nombre, IP y MAC del 'onclick'
            match = re.search(r"showElement\('([^']*)',\d+,'([^']*)','([^']*)'\)", imgTag['onclick'])
            
            if match:
                deviceName = match.group(1)  # Nombre del dispositivo
                deviceIp = match.group(2)    # Dirección IP
                deviceMac = match.group(3)   # Dirección MAC

                nameList += [deviceName]     # Añadimos nombre del dispositivo
                ipList += [deviceIp]         # Añadimos dirección IP
                macList += [deviceMac]       # Añadimos dirección MAC
                
                # Imprimimos el cada nombre, IP y MAC de cada device en el fichero correspondiente (devices_info.txt / compare_devices_info.txt)
                with open(filePath, 'a') as file:
                    file.write(f"Name: {deviceName}" + "#")
                    file.write(f"IP: {deviceIp}" + "#")
                    file.write(f"MAC: {deviceMac}" + "#\n")

    return () # Devolvemos los valores

# Comparamos los dispositivos que antes estaban conectados con los nuevos que puede haber
def compareDevices():
    print("[i] Comprobando si hay nuevos dispositivos ...\n")
    
    # Definiendo los ficheros a comparar
    principalFile = "devices_info.txt"        # Fichero con el que compararemos la nueva información
    compareFile = "compare_devices_info.txt"  # Fichero que contiene los nuevos devices conectados a la red

    # Leyendo cada fichero
    principalFileLines = readFile(principalFile)
    compareFileLines = readFile(compareFile)
    
    # Parseamos la información que nos interesa (función parseDeviceInfo())
    principalDevices = parseDeviceInfo(principalFileLines)
    compareDevices = parseDeviceInfo(compareFileLines)
    
    # Convertir listas de dispositivos a conjuntos para comparación
    set1 = set((d['Name'], d['IP'], d['MAC']) for d in principalDevices)
    set2 = set((d['Name'], d['IP'], d['MAC']) for d in compareDevices)
    
    # Comparar conjuntos
    added = set2 - set1
    
    # En caso de haber un device añadido llamamos a la función addPoints, si no hay ninguno salimos
    if added:
        # Configurando la conexión a la BD
        conn = mysql.connector.connect( 
            host='localhost',
            user='wifipointsmanager',
            password=os.getenv("MYSQL_PASSWORD"),
            database='wifipoints'
        )

        puntos = "" # Variable de control de puntos
        for device in added:
            puntos = addPoints(device, puntos, conn)

            if (puntos == "si"):
                pass
            else:
                print("[i] Nadie ha ganado puntos")
    else:
        print("[i] Nadie ha ganado puntos")
    
    return 0

# Obteniendo la información que queremos en el formato que queremos
def parseDeviceInfo(lines):
    devices = []
    for line in lines:
        # Asumimos que la línea sigue el formato "Name: <name>#IP: <ip>#MAC: <mac>#"
        parts = line.strip().split('#')
        if len(parts) >= 3:
            device_info = {}
            for part in parts:
                if ': ' in part:
                    key, value = part.split(': ', 1)
                    device_info[key] = value
            if len(device_info) == 3:
                devices.append(device_info)
    return devices

# Añadiendo los puntos a cada uno de los devices que estén definidos en la tabla players
def addPoints(device, puntos, conn):
    # Creamos un cursor
    cursor = conn.cursor()

    # Comprobamos si la persona es un jugador antes de insertarle puntos
    cursor.execute('SELECT * FROM players WHERE mac=\"' + device[2] + '\"')
    rows = cursor.fetchall()

    if not rows:
        pass # Al no haber resultados pasamos
    else:
        puntos="si" # Definimos una variable que nos indica que hemos añadido un punto

        # Comprobamos si el jugador anteriormente tenía algún punto
        # SELECT p.nick, pp.points FROM players p JOIN players_points pp ON p.nick = pp.nick WHERE p.mac = 'xx:xx:xx:xx:xx:xx';
        cursor.execute('SELECT p.nick, pp.points FROM players p JOIN players_points pp ON p.nick = pp.nick WHERE p.mac=\"' + device[2] + '\";')
        rows = cursor.fetchall()

        # Almacenamos en deviceNick el nick del jugador y en deviceName el nombre del jugador
        cursor.execute('SELECT nick, name FROM players WHERE mac = \"' + device[2] + '\";')
        result = cursor.fetchone()
        deviceNick = result[0]   
        deviceName = result[1]

        # Al ser la primera vez del jugador, le insertamos su primer punto
        if not rows:
            # Insertamos el primer punto del jugador y mostramos un mensaje
            cursor.execute('INSERT INTO players_points VALUES (\"' + deviceNick + '\", \"' + deviceName + '\", 1);')
            conn.commit()
            print("[+] " + deviceNick + " ha obtenido su primer punto")
        else:            
            # UPDATE players_points SET points = points + 1 WHERE nick = (SELECT nick FROM players WHERE mac = 'XX:XX:XX:XX:XX:XX');
            cursor.execute('UPDATE players_points SET points = points + 1 WHERE nick = (SELECT nick FROM players WHERE mac=\"' + device[2] + '\");')
            conn.commit()

            print("[+] " + deviceNick + " ha ganado un punto más")

    return(puntos)

# Efectuando backup de los archivos generados
def backupsFiles():
    print("\n[i] Realizando backup ...")
    date = datetime.now().strftime("%Y%m%d") # Fecha con AÑOMESDÍA
    dateHours = datetime.now().strftime("%Y%m%d_%H%M%S") # Fecha con AÑOMESDÍA_HORAMESSEGUNDO
    
    backupPath = "../backups"
    if not os.path.exists(backupPath): # Comprobando si existe el directorio de Backups.
        os.makedirs(backupPath) # No existe el directorio backups por lo que se crea

    completeNamePath = "../backups/" + date + "/"
    if not os.path.exists(completeNamePath): # Comprobando si existe el directorio de backups del día
        os.makedirs(completeNamePath) # No existe por lo que lo creamos

    completeFileName = "devices_info_" + dateHours + ".txt" # Nombre completo del fichero backup
    os.rename("devices_info.txt", completeNamePath + completeFileName) # Moviendo el fichero de devices a backups
    os.rename("compare_devices_info.txt", "devices_info.txt") # Quedandonos con el mapa de red actual

    print("[+] Backup guardado en ..\\backups")


if __name__ == '__main__':

    # Comprobando si las variables de entorno SESSION_KEY y/o MYSQL_PASSWORD están configuradas
    if (not os.getenv("SESSION_KEY") or (not os.getenv("MYSQL_PASSWORD"))):
        if (not os.getenv("SESSION_KEY")): # Comprobando si está definida la password para el acceso al router en la variable de entorno SESSION_KEY
            print("[!] Configura la variable de entorno SESSION_KEY con la password del router")
        if (not os.getenv("MYSQL_PASSWORD")): # Comprobando si está definida la password para el acceso al router en la variable de entorno MYSQL_PASSWORD
            print("[!] Configura la variable de entorno MYSQL_PASSWORD con la password de acceso a MySQL")

        exit(1)

    portalConnect() # Conexión al portal Wi-FI
    r = getNetworkMap() # Obtención del Mapa de Red de la Wi-Fi sobre networkmap.html

    if (os.path.isfile('devices_info.txt')): # Si existe devices_info.txt significa que se ha ejecutado anteriormente por lo que hay que comparar con la información anterior

        parseDevices(r, 'compare_devices_info.txt') # Nos quedamos con la lista de nombres, IPs y MACs de los dispositivos de la red
        compareDevices() # Comparando si hay nuevos devices
        backupsFiles() # Realiza un backup de los archivos generados
    
    else: # Al ser la primera vez que se ejecuta necesitamos quedarnos con la información del mapa de red actual
        nameList, ipList, macList = parseDevices(r, 'devices_info.txt') # Nos quedamos con la lista de nombres, IPs y MACs de los dispositivos de la red
        
        print("[+] El mapa de red se ha guardado en el fichero devices_info.txt")
        print("[i] Por favor, vuelva a ejecutarlo para ver si hay alguien que pueda ganar 1 punto más!")
