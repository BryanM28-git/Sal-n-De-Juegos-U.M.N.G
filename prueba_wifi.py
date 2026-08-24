import network
import socket
from time import sleep

# =====================================
# DATOS WIFI
# =====================================

SSID = "CASTEL PISO II"
PASSWORD = "Castel#52451888"


# =====================================
# REINICIAR WIFI
# =====================================

print("Reiniciando WiFi...")

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

# Apagar las dos interfaces
sta.active(False)
ap.active(False)

sleep(1)

# Activar solamente modo estacion
sta.active(True)

sleep(1)

# Limitar reintentos
try:
    sta.config(reconnects=3)
except:
    pass


# =====================================
# CONECTAR
# =====================================

print("Conectando a:", SSID)

sta.connect(SSID, PASSWORD)

contador = 0

while not sta.isconnected():

    estado = sta.status()

    print("Estado WiFi:", estado)

    sleep(1)

    contador += 1

    if contador >= 20:

        print("No se pudo conectar")

        sta.active(False)

        raise Exception("Error de conexion WiFi")


# =====================================
# INFORMACION
# =====================================

config = sta.ifconfig()

print("")
print("WiFi conectado!")
print("IP:", config[0])
print("Mascara:", config[1])
print("Gateway:", config[2])


# =====================================
# SERVIDOR HTTP
# =====================================

direccion = socket.getaddrinfo(
    "0.0.0.0",
    80
)[0][-1]

servidor = socket.socket()

servidor.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

servidor.bind(direccion)

servidor.listen(1)

print("")
print("Servidor iniciado")
print("Abre en tu PC:")
print("http://" + config[0])


# =====================================
# SERVIDOR
# =====================================

while True:

    cliente, direccion_cliente = servidor.accept()

    print("Conexion:", direccion_cliente)

    peticion = cliente.recv(1024)

    print(peticion)

    respuesta = """HTTP/1.1 200 OK
Content-Type: text/html
Connection: close

<html>
<head>
<title>ESP32 GAME ROOM</title>
</head>

<body>

<h1>GAME ROOM ESP32-S3</h1>

<p>Conexion WiFi funcionando correctamente.</p>

<p>PC conectado con ESP32.</p>

</body>
</html>
"""

    cliente.send(respuesta.encode())

    cliente.close()