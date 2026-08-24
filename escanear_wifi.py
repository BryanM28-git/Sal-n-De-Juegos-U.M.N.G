import network
from time import sleep

wifi = network.WLAN(network.STA_IF)

wifi.active(False)
sleep(1)

wifi.active(True)
sleep(1)

print("Buscando redes WiFi...")

redes = wifi.scan()

print("Total encontradas:", len(redes))
print()

for i, red in enumerate(redes):

    ssid_bytes = red[0]

    try:
        ssid = ssid_bytes.decode("utf-8")
    except:
        ssid = str(ssid_bytes)

    if ssid == "":
        ssid = "<RED OCULTA>"

    print(
        i,
        "|",
        ssid,
        "| Canal:",
        red[2],
        "| RSSI:",
        red[3]
    )

print()
print("ESCANEO TERMINADO")