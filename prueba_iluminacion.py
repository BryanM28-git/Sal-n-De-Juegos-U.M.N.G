from machine import Pin
from time import sleep

rojo = Pin(47, Pin.OUT)
verde = Pin(48, Pin.OUT)
azul = Pin(18, Pin.OUT)
amarillo = Pin(2, Pin.OUT)

# Apagar todo al inicio
rojo.value(0)
verde.value(0)
azul.value(0)
amarillo.value(0)

while True:

    print("ROJO")
    rojo.value(1)
    sleep(2)
    rojo.value(0)

    print("VERDE")
    verde.value(1)
    sleep(2)
    verde.value(0)

    print("AZUL")
    azul.value(1)
    sleep(2)
    azul.value(0)

    print("AMARILLO")
    amarillo.value(1)
    sleep(2)
    amarillo.value(0)