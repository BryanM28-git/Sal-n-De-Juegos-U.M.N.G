# Salón de Juegos Inteligente U.M.N.G. 🎮🤖

Este repositorio documenta el diseño, la implementación y la validación exitosa de una maqueta interactiva de un **Salón de Juegos Inteligente**. Este proyecto se desarrolló como parte de la carrera de Ingeniería Mecatrónica en la Universidad Militar Nueva Granada.

**¡Declaración de éxito!** La maqueta física y el software funcionaron a la perfección, logrando una comunicación fluida y en tiempo real entre el asistente de voz en el PC, la API de IA (DeepSeek), y todos los actuadores físicos y sensores en el microcontrolador ESP32-S3.

## 📋 Descripción General y Evidencia Física

La maqueta simula un entorno de entretenimiento automatizado. Cuenta con su propio sistema de "refrigeración" (un ventilador DC controlado por PWM), iluminación "gamer" (cuatro LEDs de colores), y una consola central (una pantalla OLED) donde el usuario puede interactuar con tres minijuegos diferentes.

Todo el sistema puede ser controlado de forma manual mediante un teclado matricial 4x4 o mediante comandos de voz utilizando un asistente virtual impulsado por la API de DeepSeek.

### Vista de la Maqueta Funcional

![Vista superior de la maqueta de cartón funcional](maqueta.jpeg)
*Maqueta funcional del Salón de Juegos Inteligente, construida en cartón, mostrando la consola central con pantalla OLED y teclado.*

---

## 🎬 Video de Funcionamiento en Acción

Puedes ver el video que demuestra todas las características de la maqueta en acción (control de voz, navegación, juegos, luces y ventilador) haciendo clic en la siguiente imagen:

[![Video demostrativo de la maqueta](https://img.youtube.com/vi/eW1v78o2a9Y/0.jpg)](https://youtube.com/shorts/eW1v78o2a9Y)

---

## 🛠️ Materiales y Hardware Utilizado

Este proyecto integra componentes clave para lograr la experiencia interactiva:

*   **Microcontrolador:** ESP32-S3 (cerebro de hardware, operando en MicroPython).
*   **Visualización:** Pantalla OLED SSD1306/SSD1309 (comunicación vía protocolo SPI).
*   **Controles de Juego:**
    *   Teclado matricial 4x4 (para navegación y juegos de tiro/reflejos).
    *   Potenciómetro analógico (para control de movimiento suave en el juego de carreras).
*   **Actuadores:**
    *   Ventilador DC controlado por PWM (Simulación de refrigeración, 3 velocidades).
    *   Diodos LED (Rojo, Verde, Azul, Amarillo) (Iluminación gamer).
*   **Interfaz de Voz:** Micrófono y altavoces conectados al PC.

---

## 📂 Arquitectura del Sistema

La solución está estructurada en dos capas principales que se sincronizan a través de comunicación Serial (UART) a 115200 baudios:

### 1. Capa de Alto Nivel (PC) - Asistente de Voz
*   **`chat_voz.py`**: Es el script central en el PC. Captura el audio del micrófono (`speech_recognition`), envía el texto a la API de **DeepSeek**, procesa la respuesta para extraer comandos y los envía vía Serial al ESP32. También usa `pyttsx3` para responder con voz sintetizada.
    *   **Prompt de IA:** El prompt del sistema para DeepSeek está diseñado para que actúe exclusivamente como el administrador del salón, filtrando intenciones para no enviar texto basura, sino comandos exactos (ej. `VENT_MAX`, `LUZ_ROJA`).

### 2. Capa Físico-Lógica (ESP32-S3) - Control de Maqueta
*   **`menu_principal.py`**: Es el núcleo del microcontrolador. Gestiona el menú en la pantalla OLED, recibe comandos seriales del PC y escanea el teclado matricial. Se encarga de encender la iluminación correspondiente, ajustar la velocidad del ventilador y lanzar el minijuego seleccionado. Utiliza una máquina de estados para una gestión de flujo robusta.
*   **Lógica de Minijuegos:**
    *   **`juego_carrera.py`**: Implementa detección geométrica de colisiones 2D donde el jugador usa el **potenciómetro analógico** para mover un auto. La dificultad aumenta dinámicamente con el puntaje.
    *   **`juego_tiro.py` / `juego_reflejos.py`**: Minijuegos de precisión donde el jugador usa el **teclado matricial** (2, 4, 6, 8) para mover una mira y disparar (tecla 5) a objetivos que aparecen aleatoriamente. Utiliza temporizadores no bloqueantes (`ticks_ms`) para calcular la precisión.

### 3. Controladores y Librerías (Drivers)
*   **`oled_game.py`**: Clase personalizada que optimiza el manejo del *FrameBuffer* de la pantalla OLED, la limpieza de memoria y el renderizado rápido de textos y formas.
*   **`ssd1306.py` / `ssd1309.py`**: Drivers de bajo nivel para manejar la pantalla OLED a través de SPI.

### 4. Scripts de Pruebas (Diagnóstico)
*   El repositorio incluye scripts (`prueba_*.py`) cruciales para el desarrollo y diagnóstico individual de cada periférico (LEDs, teclado, ventilador, pantalla, WiFi), asegurando que la maqueta final funcionara sin fallos.

---

## 🚀 Despliegue del Proyecto

Sigue estos pasos para reproducir el funcionamiento:

1.  Conectar el ESP32-S3 al PC mediante USB.
2.  Cargar todos los archivos de MicroPython al microcontrolador (excepto `chat_voz.py`).
3.  Configurar la variable `API_KEY` de DeepSeek en el entorno de Python en el PC (archivo `.env` o en el código).
4.  Ejecutar `menu_principal.py` en el microcontrolador.
5.  Iniciar `chat_voz.py` en el terminal del PC.
6.  ¡Comienza a interactuar! Di "enciende las luces", "activa la refrigeración" o "inicia un juego de carreras".

## 👤 Autor

**Bryan Martínez**
Estudiante de Ingeniería Mecatrónica, Universidad Militar Nueva Granada.
