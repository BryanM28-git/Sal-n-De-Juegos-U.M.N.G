from machine import Pin
from time import sleep

filas = [
    Pin(35, Pin.OUT),
    Pin(36, Pin.OUT),
    Pin(37, Pin.OUT),
    Pin(38, Pin.OUT)
]

columnas = [
    Pin(40, Pin.IN, Pin.PULL_UP),  # C1
    Pin(39, Pin.IN, Pin.PULL_UP),  # C2
    Pin(41, Pin.IN, Pin.PULL_UP),  # C3
    Pin(42, Pin.IN, Pin.PULL_UP)   # C4
]

teclas = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

for fila in filas:
    fila.value(1)


def leer_teclado():

    for i in range(4):

        # apagar todas las filas
        for fila in filas:
            fila.value(1)

        # activar una fila
        filas[i].value(0)

        for j in range(4):

            if columnas[j].value() == 0:

                tecla = teclas[i][j]

                while columnas[j].value() == 0:
                    sleep(0.02)

                return tecla

    return None


print("Teclado listo")

while True:

    tecla = leer_teclado()

    if tecla is not None:
        print("Tecla:", tecla)

    sleep(0.02)