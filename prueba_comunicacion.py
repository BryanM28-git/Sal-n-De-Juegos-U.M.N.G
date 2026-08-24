import sys
import select
from machine import Pin, PWM
from time import sleep


# =====================================
# ILUMINACION
# =====================================

luz_roja = Pin(47, Pin.OUT)
luz_verde = Pin(48, Pin.OUT)
luz_azul = Pin(18, Pin.OUT)
luz_amarilla = Pin(2, Pin.OUT)


def apagar_luces():
    luz_roja.value(0)
    luz_verde.value(0)
    luz_azul.value(0)
    luz_amarilla.value(0)


def luces_rojas():
    apagar_luces()
    luz_roja.value(1)


def luces_verdes():
    apagar_luces()
    luz_verde.value(1)


def luces_azules():
    apagar_luces()
    luz_azul.value(1)


def luces_amarillas():
    apagar_luces()
    luz_amarilla.value(1)


# =====================================
# VENTILADOR
# =====================================

ventilador = PWM(Pin(21))
ventilador.freq(1000)


def vent_off():
    ventilador.duty_u16(0)


def vent_on():
    ventilador.duty_u16(52000)


def vent_bajo():
    ventilador.duty_u16(40000)


def vent_medio():
    ventilador.duty_u16(52000)


def vent_max():
    ventilador.duty_u16(65535)


# =====================================
# ESTADO INICIAL
# =====================================

apagar_luces()
vent_off()

print("ESP32 LISTA PARA COMANDOS")


# =====================================
# PRUEBA AUTOMATICA AL INICIAR
# =====================================

print("Probando luz amarilla...")
luz_amarilla.value(1)
sleep(1)
luz_amarilla.value(0)

print("Probando ventilador...")
vent_max()
sleep(1)
vent_off()

print("Prueba inicial terminada")


# =====================================
# COMUNICACION SERIAL
# =====================================

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)


while True:

    eventos = poll.poll(100)

    if eventos:

        comando = sys.stdin.readline().strip()

        if comando:

            print("RECIBIDO:", comando)

            # -------------------------
            # VENTILADOR
            # -------------------------

            if comando == "VENT_ON":

                vent_on()
                print("OK: VENTILADOR ENCENDIDO")

            elif comando == "VENT_OFF":

                vent_off()
                print("OK: VENTILADOR APAGADO")

            elif comando == "VENT_BAJO":

                vent_bajo()
                print("OK: VENTILADOR BAJO")

            elif comando == "VENT_MEDIO":

                vent_medio()
                print("OK: VENTILADOR MEDIO")

            elif comando == "VENT_MAX":

                vent_max()
                print("OK: VENTILADOR MAXIMO")


            # -------------------------
            # LUCES
            # -------------------------

            elif comando == "LUZ_ROJA":

                luces_rojas()
                print("OK: LUZ ROJA")

            elif comando == "LUZ_VERDE":

                luces_verdes()
                print("OK: LUZ VERDE")

            elif comando == "LUZ_AZUL":

                luces_azules()
                print("OK: LUZ AZUL")

            elif comando == "LUZ_AMARILLA":

                luces_amarillas()
                print("OK: LUZ AMARILLA")


            # -------------------------
            # COMANDO DESCONOCIDO
            # -------------------------

            else:

                print(
                    "ERROR: COMANDO DESCONOCIDO:",
                    comando
                )

    sleep(0.01)