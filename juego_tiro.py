from machine import Pin
from time import sleep, ticks_ms, ticks_diff
from random import randint

from oled_game import OLED_Game


# =========================
# OLED
# =========================

oled = OLED_Game()


# =========================
# TECLADO
# =========================

filas = [
    Pin(35, Pin.OUT),
    Pin(36, Pin.OUT),
    Pin(37, Pin.OUT),
    Pin(38, Pin.OUT)
]

# C1 y C2 están intercambiadas físicamente en tu teclado
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


# =========================
# CONFIGURACION
# =========================

ANCHO = 128
ALTO = 64

DURACION = 30

# Menor valor = movimiento más suave
PASO_MIRA = 2

RADIO_OBJETIVO = 4


# =========================
# LECTURA DEL TECLADO
# =========================

def leer_teclado():

    for i in range(4):

        # Desactivar todas las filas
        for fila in filas:
            fila.value(1)

        # Activar una fila
        filas[i].value(0)

        for j in range(4):

            if columnas[j].value() == 0:
                return teclas[i][j]

    return None


def esperar_soltar_tecla(tecla_buscada):

    while leer_teclado() == tecla_buscada:
        sleep(0.02)


# =========================
# OBJETIVO
# =========================

def nuevo_objetivo():

    x = randint(10, 117)
    y = randint(17, 54)

    return x, y


def dibujar_objetivo(x, y):

    # Objetivo cuadrado para máxima compatibilidad
    oled.frame.rect(
        x - 4,
        y - 4,
        9,
        9,
        1
    )

    oled.frame.rect(
        x - 2,
        y - 2,
        5,
        5,
        1
    )

    oled.frame.pixel(
        x,
        y,
        1
    )


# =========================
# MIRA
# =========================

def dibujar_mira(x, y):

    oled.frame.hline(
        x - 4,
        y,
        9,
        1
    )

    oled.frame.vline(
        x,
        y - 4,
        9,
        1
    )

    # Centro vacío para diferenciar la mira
    oled.frame.pixel(
        x,
        y,
        0
    )


# =========================
# DISPARO
# =========================

def comprobar_disparo(
    mira_x,
    mira_y,
    objetivo_x,
    objetivo_y
):

    distancia_x = abs(
        mira_x - objetivo_x
    )

    distancia_y = abs(
        mira_y - objetivo_y
    )

    if (
        distancia_x <= RADIO_OBJETIVO
        and
        distancia_y <= RADIO_OBJETIVO
    ):
        return True

    return False


# =========================
# PANTALLA INICIAL
# =========================

def pantalla_inicio():

    oled.limpiar()

    oled.texto(
        "TIRO AL BLANCO",
        8,
        6
    )

    oled.texto(
        "2 = ARRIBA",
        18,
        20
    )

    oled.texto(
        "4   5   6",
        25,
        32
    )

    oled.texto(
        "8 = ABAJO",
        18,
        44
    )

    oled.texto(
        "5 = DISPARAR",
        12,
        56
    )

    oled.mostrar()

    sleep(3)

    for numero in [3, 2, 1]:

        oled.limpiar()

        oled.texto(
            "PREPARATE",
            28,
            10
        )

        oled.texto(
            str(numero),
            60,
            35
        )

        oled.mostrar()

        sleep(1)


# =========================
# MENSAJES
# =========================

def mensaje_acierto():

    oled.frame.fill(0)

    oled.frame.text(
        "ACIERTO!",
        34,
        24,
        1
    )

    oled.frame.text(
        "+1 PUNTO",
        30,
        39,
        1
    )

    oled.mostrar()

    sleep(0.30)


def mensaje_fallo():

    oled.frame.fill(0)

    oled.frame.text(
        "FALLASTE!",
        30,
        28,
        1
    )

    oled.mostrar()

    sleep(0.20)


def game_over(puntos, disparos):

    oled.limpiar()

    oled.texto(
        "TIEMPO!",
        36,
        4
    )

    oled.texto(
        "Puntos: " + str(puntos),
        15,
        20
    )

    oled.texto(
        "Disparos: " + str(disparos),
        8,
        33
    )

    if disparos > 0:

        precision = int(
            puntos * 100 / disparos
        )

        oled.texto(
            "Precision:" + str(precision) + "%",
            4,
            48
        )

    else:

        oled.texto(
            "Precision:0%",
            10,
            48
        )

    oled.mostrar()


# =========================
# JUEGO PRINCIPAL
# =========================

def jugar_tiro():

    pantalla_inicio()

    puntos = 0
    disparos = 0

    # Mira comienza en el centro
    mira_x = 64
    mira_y = 38

    objetivo_x, objetivo_y = nuevo_objetivo()

    inicio = ticks_ms()

    jugando = True

    while jugando:

        # -------------------------
        # TIEMPO
        # -------------------------

        transcurrido = ticks_diff(
            ticks_ms(),
            inicio
        )

        segundos = transcurrido // 1000

        restante = DURACION - segundos

        if restante <= 0:
            jugando = False
            break

        # -------------------------
        # LEER TECLADO
        # -------------------------

        tecla = leer_teclado()

        # ARRIBA
        if tecla == "2":

            mira_y -= PASO_MIRA

            if mira_y < 17:
                mira_y = 17

        # ABAJO
        elif tecla == "8":

            mira_y += PASO_MIRA

            if mira_y > 58:
                mira_y = 58

        # IZQUIERDA
        elif tecla == "4":

            mira_x -= PASO_MIRA

            if mira_x < 6:
                mira_x = 6

        # DERECHA
        elif tecla == "6":

            mira_x += PASO_MIRA

            if mira_x > 121:
                mira_x = 121

        # -------------------------
        # DISPARAR
        # -------------------------

        elif tecla == "5":

            disparos += 1

            if comprobar_disparo(
                mira_x,
                mira_y,
                objetivo_x,
                objetivo_y
            ):

                puntos += 1

                mensaje_acierto()

                objetivo_x, objetivo_y = (
                    nuevo_objetivo()
                )

            else:

                mensaje_fallo()

            # Evita disparos automáticos
            # al mantener presionado 5
            esperar_soltar_tecla("5")

        # -------------------------
        # DIBUJAR PANTALLA
        # -------------------------

        oled.frame.fill(0)

        # Puntuación
        oled.frame.text(
            "P:" + str(puntos),
            2,
            2,
            1
        )

        # Tiempo
        oled.frame.text(
            "T:" + str(restante),
            96,
            2,
            1
        )

        # Separador superior
        oled.frame.hline(
            0,
            11,
            128,
            1
        )

        # Objetivo
        dibujar_objetivo(
            objetivo_x,
            objetivo_y
        )

        # Mira
        dibujar_mira(
            mira_x,
            mira_y
        )

        oled.mostrar()

        # Controla la velocidad del movimiento
        sleep(0.035)

    game_over(
        puntos,
        disparos
    )


# =========================
# EJECUCION
# =========================

if __name__ == "__main__":
    jugar_tiro()