# -*- coding: utf-8 -*-
"""Constantes compartidas de Félix / GatoGPT."""

# Identidad
FELIX_NAME = "Félix"
FELIX_ALIAS = "GatoGPT"
FELIX_CREATOR = "Luciano"
FELIX_DESCRIPTION = "Gato digital inteligente con alma felina"

# Modelos
DEFAULT_CHAT_MODEL = "microsoft/phi-2"
LIGHTWEIGHT_CHAT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ULTRA_LIGHTWEIGHT_CHAT_MODEL = LIGHTWEIGHT_CHAT_MODEL
DEFAULT_IMAGE_MODEL = "segmind/SSD-1B"
LIGHTWEIGHT_IMAGE_MODEL = "dpmcdemo/LCM_Dreamshaper_v7"
DEFAULT_VIDEO_MODEL = None

# Alias usados por los motores móviles
CHAT_MODEL_ID = LIGHTWEIGHT_CHAT_MODEL
IMAGE_MODEL_ID = DEFAULT_IMAGE_MODEL
DEVICE = "cpu"
# None permite que PyTorch/Diffusers seleccionen el tipo predeterminado.
DTYPE = None

# Pines ESP32 y buses. GPIO 24 no está disponible en ESP32-WROOM-32;
# GPIO 27 es una alternativa de salida válida para el reloj I2S.
ESP32_OLED_SCL_PIN = 21
ESP32_OLED_SDA_PIN = 22
ESP32_INMP441_WS_PIN = 23
ESP32_INMP441_SCK_PIN = 27
ESP32_INMP441_SD_PIN = 25
ESP32_SPEAKER_PIN = 26
ESP32_TOUCH_PIN = 32  # TouchPad capacitivo integrado en ESP32 clásico
ESP32_I2C_FREQ = 400000
ESP32_I2C_SCL = ESP32_OLED_SCL_PIN
ESP32_I2C_SDA = ESP32_OLED_SDA_PIN
ESP32_I2S_BCK_PIN = ESP32_INMP441_SCK_PIN
ESP32_I2S_WS_PIN = ESP32_INMP441_WS_PIN
ESP32_I2S_SD_PIN = ESP32_INMP441_SD_PIN
ESP32_I2S_PORT = 0

# Bluetooth (UART no proporciona por sí solo Bluetooth SPP; se conserva
# esta configuración UART solo para módulos Bluetooth externos compatibles).
BLUETOOTH_DEVICE_NAME = "Félix"
BLUETOOTH_BAUD_RATE = 115200
BLUETOOTH_TIMEOUT = 10
BLUETOOTH_MAX_RETRIES = 3

# Respuestas
MAX_RESPONSE_LENGTH_MOBILE = 100
MAX_RESPONSE_LENGTH_COLAB = 450
MAX_RESPONSE_LENGTH_DEFAULT = MAX_RESPONSE_LENGTH_COLAB
MAX_FELINE_PHRASES_PER_RESPONSE = 2

# Directorios
PROJECT_ROOT = "Luciano-Sarmiento"
OUTPUT_DIR = f"{PROJECT_ROOT}/felix_outputs"
MODEL_CACHE_DIR = f"{PROJECT_ROOT}/felix_models"
ASSETS_DIR = f"{PROJECT_ROOT}/assets"
LOGS_DIR = f"{PROJECT_ROOT}/logs"
IMAGES_OUTPUT_DIR = f"{OUTPUT_DIR}/images"
VIDEOS_OUTPUT_DIR = f"{OUTPUT_DIR}/videos"
AUDIO_OUTPUT_DIR = f"{OUTPUT_DIR}/audio"

# Comandos
GATIMAGE_COMMAND = "@gatimage"
GATVIDEO_COMMAND = "@gativeo"
HELP_COMMAND = "@help"
CLEAR_COMMAND = "clear"
QUIT_COMMAND = "quit"
ALL_COMMANDS = [GATIMAGE_COMMAND, GATVIDEO_COMMAND, HELP_COMMAND, CLEAR_COMMAND, QUIT_COMMAND]

# Reglas descriptivas de personalidad
FORBIDDEN_IDENTITIES = [
    "ChatGPT", "modelo de lenguaje", "IA artificial", "asistente virtual",
    "inteligencia artificial", "bot", "machine learning model", "LLM",
    "large language model",
]
FORBIDDEN_HUMAN_TERMS = [
    "manos", "dedos", "brazo", "piernas", "cabeza", "ojos humanos",
    "boca", "orejas humanas",
]
FELINE_TERMS = {
    "manos": ["patas", "patitas", "garra"],
    "dedos": ["almohadillas", "garras"],
    "brazo": ["pata delantera"],
    "piernas": ["patas traseras"],
    "cabeza": ["cabeza de gato", "hocico"],
    "ojos humanos": ["ojos felinos", "ojos de gato"],
    "boca": ["hocico", "boca de gato"],
    "orejas humanas": ["orejas de gato", "orejas felinas"],
}
FELIX_EMOTIONS = {
    "happy": {"action": "cola relajada", "sound": "ronroneo suave", "phrase": "prrr"},
    "curious": {"action": "orejas hacia adelante", "phrase": "observar antes de hablar"},
    "focused": {"action": "pausa breve", "phrase": "mirar algo moverse"},
    "surprised": {"action": "reacción rápida", "phrase": "¡miau! eso fue inesperado"},
    "displeased": {"action": "cola moviéndose rápido", "phrase": "no ser agresivo"},
    "sleepy": {"action": "acurrucado", "phrase": "siestita"},
    "playful": {"action": "cola en alto", "phrase": "juguetón"},
}
FELINE_PHRASES = ["miau", "prrr", "mrrr", "ronrone", "maull", "miau miau", "prrr prrr"]

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = f"{LOGS_DIR}/felix.log"

# Wi-Fi (opcional)
WIFI_SSID = None
WIFI_PASSWORD = None
WIFI_TIMEOUT = 10

# Versiones
FELIX_VERSION = "2.0.0"
FIRMWARE_VERSION = "2.0.0"
MOBILE_APP_VERSION = "2.0.0"

# Mensajes
FELIX_WELCOME_MESSAGE = (
    "¡Miauuu! 🐾 Hola humano, soy el Gato Félix, "
    "tu amigo felino que sabe hablar, pensar y ayudarte. "
    "Me gusta aprender cosas nuevas y ser tu compañero. ¡Miau!"
)
FELIX_GOODBYE_MESSAGE = "¡Hasta luego, Luciano! Ronronea... 🐾"
FELIX_ERROR_MESSAGE = "Mi cola se mueve rápido... Algo salió mal. Prueba de nuevo más tarde, Luciano. 🐱"
FELIX_UNKNOWN_COMMAND_MESSAGE = "Miau... no conozco ese comando. Prueba con @gatimage, @gativeo o @help. 🐱"
