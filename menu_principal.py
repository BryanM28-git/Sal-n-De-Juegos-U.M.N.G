import sys
import select

from machine import Pin, PWM
from time import sleep

from oled_game import OLED_Game

from juego_reflejos import jugar_reflejos
from juego_carrera import jugar_carrera
from juego_tiro import jugar_tiro


# =====================================
# OLED
# =====================================

oled = OLED_Game()


# =====================================
# ILUMINACION GAMER
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


def modo_menu():
    apagar_luces()
    luz_amarilla.value(1)


def modo_reflejos():
    apagar_luces()
    luz_azul.value(1)


def modo_carrera():
    apagar_luces()
    luz_verde.value(1)


def modo_tiro():
    apagar_luces()
    luz_roja.value(1)


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
# REFRIGERACION
# =====================================

ventilador = PWM(Pin(21))
ventilador.freq(1000)


def ventilador_apagado():
    ventilador.duty_u16(0)


def ventilador_bajo():
    ventilador.duty_u16(40000)


def ventilador_medio():
    ventilador.duty_u16(52000)


def ventilador_maximo():
    ventilador.duty_u16(65535)


# =====================================
# TECLADO MATRICIAL
# =====================================

filas = [
    Pin(35, Pin.OUT),
    Pin(36, Pin.OUT),
    Pin(37, Pin.OUT),
    Pin(38, Pin.OUT)
]

columnas = [
    Pin(39, Pin.IN, Pin.PULL_UP),
    Pin(40, Pin.IN, Pin.PULL_UP),
    Pin(41, Pin.IN, Pin.PULL_UP),
    Pin(42, Pin.IN, Pin.PULL_UP)
]

teclas = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

for fila in filas:
    fila.value(1)


# =====================================
# COMUNICACION USB / SERIAL
# =====================================

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)


def leer_serial():

    eventos = poll.poll(0)

    if eventos:

        comando = sys.stdin.readline().strip()

        if comando:

            print("VOZ/PC:", comando)

            return comando

    return None


# =====================================
# PROCESAR COMANDOS GENERALES
# =====================================

def procesar_comando_general(comando):

    # -------------------------
    # VENTILADOR
    # -------------------------

    if comando == "VENT_ON":

        ventilador_medio()
        print("OK: VENTILADOR ENCENDIDO")
        return True

    elif comando == "VENT_OFF":

        ventilador_apagado()
        print("OK: VENTILADOR APAGADO")
        return True

    elif comando == "VENT_BAJO":

        ventilador_bajo()
        print("OK: VENTILADOR BAJO")
        return True

    elif comando == "VENT_MEDIO":

        ventilador_medio()
        print("OK: VENTILADOR MEDIO")
        return True

    elif comando == "VENT_MAX":

        ventilador_maximo()
        print("OK: VENTILADOR MAXIMO")
        return True


    # -------------------------
    # LUCES
    # -------------------------

    elif comando == "LUZ_ROJA":

        luces_rojas()
        print("OK: LUZ ROJA")
        return True

    elif comando == "LUZ_VERDE":

        luces_verdes()
        print("OK: LUZ VERDE")
        return True

    elif comando == "LUZ_AZUL":

        luces_azules()
        print("OK: LUZ AZUL")
        return True

    elif comando == "LUZ_AMARILLA":

        luces_amarillas()
        print("OK: LUZ AMARILLA")
        return True

    return False


# =====================================
# LEER TECLADO
# =====================================

def leer_teclado():

    for i in range(4):

        for fila in filas:
            fila.value(1)

        filas[i].value(0)

        for j in range(4):

            if columnas[j].value() == 0:

                tecla = teclas[i][j]

                while columnas[j].value() == 0:
                    sleep(0.02)

                return tecla

    return None


# =====================================
# BIENVENIDA
# =====================================

def bienvenida():

    modo_menu()
    ventilador_apagado()

    oled.limpiar()

    oled.texto("GAME ROOM", 28, 8)
    oled.texto("ESP32-S3", 32, 25)
    oled.texto("INICIANDO...", 20, 43)

    oled.mostrar()

    sleep(2)


# =====================================
# MENU PRINCIPAL
# =====================================

def mostrar_menu():

    modo_menu()
    ventilador_apagado()

    oled.limpiar()

    oled.texto("GAME ROOM", 28, 2)

    oled.frame.hline(
        0,
        12,
        128,
        1
    )

    oled.texto("1. REFLEJOS", 10, 18)
    oled.texto("2. CARRERA", 10, 31)
    oled.texto("3. TIRO", 10, 44)
    oled.texto("ELIGE: 1 2 3", 8, 56)

    oled.mostrar()


# =====================================
# PANTALLA CARGANDO
# =====================================

def cargando(nombre):

    oled.limpiar()

    oled.texto("CARGANDO...", 24, 15)
    oled.texto(nombre, 30, 35)

    oled.mostrar()

    sleep(0.8)


# =====================================
# ESPERAR CONTINUAR
# =====================================

def esperar_continuar():

    while True:

        # Teclado
        tecla = leer_teclado()

        if tecla == "5":
            return


        # PC / Voz
        comando = leer_serial()

        if comando:

            # Decir MENU también permite continuar
            if comando == "MENU":
                return

            procesar_comando_general(comando)

        sleep(0.02)


# =====================================
# MENU FIN DE JUEGO
# =====================================

def menu_fin_juego():

    oled.limpiar()

    oled.texto("FIN DEL JUEGO", 12, 6)

    oled.frame.hline(
        0,
        17,
        128,
        1
    )

    oled.texto("1. JUGAR OTRA", 8, 27)
    oled.texto("2. VOLVER MENU", 5, 43)

    oled.mostrar()

    while True:

        # -------------------------
        # TECLADO
        # -------------------------

        tecla = leer_teclado()

        if tecla == "1":
            return "REPETIR"

        elif tecla == "2":
            return "MENU"


        # -------------------------
        # VOZ / PC
        # -------------------------

        comando = leer_serial()

        if comando == "MENU":
            return "MENU"

        elif comando in (
            "JUEGO_REFLEJOS",
            "JUEGO_CARRERA",
            "JUEGO_TIRO"
        ):

            # Aquí simplemente regresamos al menú.
            # Desde el menú podrá abrirse el nuevo juego.
            return "MENU"

        elif comando:

            procesar_comando_general(comando)

        sleep(0.02)


# =====================================
# OPCION INVALIDA
# =====================================

def opcion_invalida():

    oled.limpiar()

    oled.texto("OPCION", 38, 20)
    oled.texto("NO VALIDA", 28, 35)

    oled.mostrar()

    sleep(1)


# =====================================
# JUEGO 1 - REFLEJOS
# =====================================

def ejecutar_reflejos():

    while True:

        modo_reflejos()
        ventilador_bajo()

        cargando("REFLEJOS")

        jugar_reflejos()

        esperar_continuar()

        opcion = menu_fin_juego()

        if opcion == "MENU":

            ventilador_apagado()
            modo_menu()

            break


# =====================================
# JUEGO 2 - CARRERA
# =====================================

def ejecutar_carrera():

    while True:

        modo_carrera()
        ventilador_medio()

        cargando("CARRERA")

        jugar_carrera()

        esperar_continuar()

        opcion = menu_fin_juego()

        if opcion == "MENU":

            ventilador_apagado()
            modo_menu()

            break


# =====================================
# JUEGO 3 - TIRO
# =====================================

def ejecutar_tiro():

    while True:

        modo_tiro()
        ventilador_maximo()

        cargando("TIRO")

        jugar_tiro()

        esperar_continuar()

        opcion = menu_fin_juego()

        if opcion == "MENU":

            ventilador_apagado()
            modo_menu()

            break


# =====================================
# PROGRAMA PRINCIPAL
# =====================================

bienvenida()


while True:

    mostrar_menu()

    seleccion = None


    while seleccion is None:

        # =================================
        # CONTROL POR TECLADO
        # =================================

        tecla = leer_teclado()

        if tecla == "1":
            seleccion = "REFLEJOS"

        elif tecla == "2":
            seleccion = "CARRERA"

        elif tecla == "3":
            seleccion = "TIRO"


        # =================================
        # CONTROL POR VOZ / SERIAL
        # =================================

        comando = leer_serial()

        if comando:

            if comando == "JUEGO_REFLEJOS":

                seleccion = "REFLEJOS"

            elif comando == "JUEGO_CARRERA":

                seleccion = "CARRERA"

            elif comando == "JUEGO_TIRO":

                seleccion = "TIRO"

            elif comando == "MENU":

                mostrar_menu()

            else:

                procesar_comando_general(comando)


        sleep(0.02)


    # =====================================
    # ABRIR JUEGO
    # =====================================

    if seleccion == "REFLEJOS":

        ejecutar_reflejos()

    elif seleccion == "CARRERA":

        ejecutar_carrera()

    elif seleccion == "TIRO":

        ejecutar_tiro() 