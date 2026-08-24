from machine import Pin
from time import sleep

# LEDs
led_rojo = Pin(9, Pin.OUT)
led_verde = Pin(11, Pin.OUT)
led_azul = Pin(13, Pin.OUT)
led_amarillo = Pin(16, Pin.OUT)

# Pulsadores
boton_rojo = Pin(10, Pin.IN, Pin.PULL_UP)
boton_verde = Pin(12, Pin.IN, Pin.PULL_UP)
boton_azul = Pin(14, Pin.IN, Pin.PULL_UP)
boton_amarillo = Pin(17, Pin.IN, Pin.PULL_UP)

print("Prueba de los cuatro botones")
print("Presiona cada boton")

while True:

    led_rojo.value(not boton_rojo.value())
    led_verde.value(not boton_verde.value())
    led_azul.value(not boton_azul.value())
    led_amarillo.value(not boton_amarillo.value())

    sleep(0.02)