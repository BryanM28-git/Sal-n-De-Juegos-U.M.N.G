import requests
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import wave
import os
import serial
import time

# =====================================
# CONFIGURACION DEEPSEEK
# =====================================

API_KEY = ""
API_URL = "https://api.deepseek.com/v1/chat/completions"

# ==============================
# ESP32
# ==============================

PUERTO_ESP32 = "COM5"

esp32 = serial.Serial(
    PUERTO_ESP32,
    115200,
    timeout=1
)

time.sleep(2)

def enviar_esp32(comando):

    try:
        esp32.write((comando + "\n").encode())
        print("Enviado a ESP32:", comando)

    except Exception as error:
        print("Error enviando a ESP32:", error)

# =====================================
# VOZ DEL COMPUTADOR
# =====================================

engine = pyttsx3.init()
engine.setProperty("rate", 150)


def hablar(texto):

    print("Chatbot:", texto)

    engine.say(texto)
    engine.runAndWait()


# =====================================
# ESCUCHAR MICROFONO
# =====================================

def escuchar_microfono():

    frecuencia = 44100
    duracion = 5

    archivo = "audio_temp.wav"

    print()
    print("Escuchando...")

    try:

        audio = sd.rec(
            int(duracion * frecuencia),
            samplerate=frecuencia,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        with wave.open(archivo, "wb") as wf:

            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(frecuencia)
            wf.writeframes(audio.tobytes())

        reconocedor = sr.Recognizer()

        with sr.AudioFile(archivo) as source:

            audio_sr = reconocedor.record(source)

        texto = reconocedor.recognize_google(
            audio_sr,
            language="es-ES"
        )

        print("Tu:", texto)

        if os.path.exists(archivo):
            os.remove(archivo)

        return texto

    except sr.UnknownValueError:

        print("No entendi lo que dijiste.")

        if os.path.exists(archivo):
            os.remove(archivo)

        return ""

    except Exception as error:

        print("Error:", error)

        if os.path.exists(archivo):
            os.remove(archivo)

        return ""


# =====================================
# CONSULTAR A DEEPSEEK
# =====================================

def procesar_texto(texto):

    instrucciones = """
Eres el asistente de voz de un salon de juegos inteligente.

El sistema tiene:
- Juego de reflejos
- Juego de carrera
- Juego de tiro al blanco
- Iluminacion roja, verde, azul y amarilla
- Sistema de refrigeracion con ventilador

Si el usuario da una orden relacionada con el sistema,
responde SOLO con uno de estos comandos:

JUEGO_REFLEJOS
JUEGO_CARRERA
JUEGO_TIRO
VENT_ON
VENT_OFF
VENT_BAJO
VENT_MEDIO
VENT_MAX
LUZ_ROJA
LUZ_VERDE
LUZ_AZUL
LUZ_AMARILLA
MENU

Si el usuario simplemente quiere conversar,
responde normalmente en español.

No inventes otros comandos.
"""

    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }

    datos = {
        "model": "deepseek-chat",

        "messages": [
            {
                "role": "system",
                "content": instrucciones
            },
            {
                "role": "user",
                "content": texto
            }
        ]
    }

    try:

        respuesta = requests.post(
            API_URL,
            headers=headers,
            json=datos,
            timeout=20
        )

        respuesta.raise_for_status()

        resultado = respuesta.json()

        return resultado[
            "choices"
        ][0][
            "message"
        ][
            "content"
        ].strip()

    except Exception as error:

        print(
            "Error comunicando con DeepSeek:",
            error
        )

        return "ERROR"


# =====================================
# SIMULAR ACCIONES
# =====================================

def ejecutar_comando(comando):

    if comando == "JUEGO_REFLEJOS":

        enviar_esp32("JUEGO_REFLEJOS")
        hablar("Iniciando juego de reflejos.")


    elif comando == "JUEGO_CARRERA":

        enviar_esp32("JUEGO_CARRERA")
        hablar("Iniciando juego de carrera.")


    elif comando == "JUEGO_TIRO":

        enviar_esp32("JUEGO_TIRO")
        hablar("Iniciando tiro al blanco.")


    # VENTILADOR
    elif comando == "VENT_ON":
        enviar_esp32("VENT_ON")
        hablar("Refrigeracion encendida.")

    elif comando == "VENT_OFF":
        enviar_esp32("VENT_OFF")
        hablar("Refrigeracion apagada.")

    elif comando == "VENT_BAJO":
        enviar_esp32("VENT_BAJO")
        hablar("Ventilador en velocidad baja.")

    elif comando == "VENT_MEDIO":
        enviar_esp32("VENT_MEDIO")
        hablar("Ventilador en velocidad media.")

    elif comando == "VENT_MAX":
        enviar_esp32("VENT_MAX")
        hablar("Ventilador al maximo.")


    # LUCES
    elif comando == "LUZ_ROJA":
        enviar_esp32("LUZ_ROJA")
        hablar("Iluminacion roja activada.")

    elif comando == "LUZ_VERDE":
        enviar_esp32("LUZ_VERDE")
        hablar("Iluminacion verde activada.")

    elif comando == "LUZ_AZUL":
        enviar_esp32("LUZ_AZUL")
        hablar("Iluminacion azul activada.")

    elif comando == "LUZ_AMARILLA":
        enviar_esp32("LUZ_AMARILLA")
        hablar("Iluminacion amarilla activada.")

    elif comando == "MENU":

        enviar_esp32("MENU")
        hablar("Regresando al menu principal.")

    elif comando == "ERROR":
        hablar("No pude comunicarme con el asistente.")

    else:
        hablar(comando)


# =====================================
# PROGRAMA PRINCIPAL
# =====================================

def main():

    hablar(
        "Asistente del salon de juegos iniciado."
    )

    while True:

        texto = escuchar_microfono()

        if not texto:
            continue

        texto_minuscula = texto.lower()

        if "salir" in texto_minuscula:

            hablar(
                "Cerrando el asistente. Hasta luego."
            )

            break

        respuesta = procesar_texto(texto)

        print(
            "DeepSeek:",
            respuesta
        )

        ejecutar_comando(
            respuesta
        )


if __name__ == "__main__":
    main()