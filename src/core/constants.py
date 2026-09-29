# -*- coding: utf-8 -*-
"""
Constantes Globales para Félix / GatoGPT

Este módulo centraliza todas las constantes usadas en el proyecto
para garantizar consistencia entre todos los módulos.

Uso:
    from src.core.constants import (
        MAX_RESPONSE_LENGTH,
        DEFAULT_CHAT_MODEL,
        DEFAULT_IMAGE_MODEL,
        FELIX_NAME,
    )
"""

# =============================================================================
# IDENTIDAD DE FÉLIX
# =============================================================================

FELIX_NAME = "Félix"
FELIX_ALIAS = "GatoGPT"
FELIX_CREATOR = "Luciano"
FELIX_DESCRIPTION = "Gato digital inteligente con alma felina"

# =============================================================================
# CONFIGURACIÓN DE MODELOS DE IA
# =============================================================================

# Modelos de chat (para respuestas de texto)
DEFAULT_CHAT_MODEL = "microsoft/phi-2"  # 2.7B params
LIGHTWEIGHT_CHAT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # 1.1B params
ULTRA_LIGHTWEIGHT_CHAT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Para dispositivos con poca RAM

# Modelos de imágenes (para @gatimage)
DEFAULT_IMAGE_MODEL = "segmind/SSD-1B"  # 1B params
LIGHTWEIGHT_IMAGE_MODEL = "dpmcdemo/LCM_Dreamshaper_v7"  # Más ligero

# Modelos de video (para @gativeo - experimental)
DEFAULT_VIDEO_MODEL = None  # Por implementar

# =============================================================================
# CONFIGURACIÓN DE HARDWARE
# =============================================================================

# Pines del ESP32 (por defecto)
ESP32_OLED_SCL_PIN = 21
ESP32_OLED_SDA_PIN = 22
ESP32_INMP441_WS_PIN = 23
ESP32_INMP441_SCK_PIN = 24
ESP32_INMP441_SD_PIN = 25
ESP32_SPEAKER_PIN = 26

# Configuración I2C para OLED
ESP32_I2C_FREQ = 400000  # 400 kHz
ESP32_I2C_SCL = ESP32_OLED_SCL_PIN
ESP32_I2C_SDA = ESP32_OLED_SDA_PIN

# Configuración I2S para INMP441
ESP32_I2S_BCK_PIN = ESP32_INMP441_SCK_PIN
ESP32_I2S_WS_PIN = ESP32_INMP441_WS_PIN
ESP32_I2S_SD_PIN = ESP32_INMP441_SD_PIN
ESP32_I2S_PORT = 0  # Puerto I2S del ESP32

# =============================================================================
# CONFIGURACIÓN DE BLUETOOTH
# =============================================================================

BLUETOOTH_DEVICE_NAME = "Félix"
BLUETOOTH_BAUD_RATE = 115200
BLUETOOTH_TIMEOUT = 10  # segundos
BLUETOOTH_MAX_RETRIES = 3

# =============================================================================
# CONFIGURACIÓN DE RESPUESTAS
# =============================================================================

# Longitud máxima de respuestas
MAX_RESPONSE_LENGTH_MOBILE = 100  # palabras
MAX_RESPONSE_LENGTH_COLAB = 450  # palabras
MAX_RESPONSE_LENGTH_DEFAULT = MAX_RESPONSE_LENGTH_COLAB

# Número máximo de frases felinas por respuesta
MAX_FELINE_PHRASES_PER_RESPONSE = 2

# =============================================================================
# CONFIGURACIÓN DE ARCHIVOS Y DIRECTORIOS
# =============================================================================

# Directorios relativos al proyecto
PROJECT_ROOT = "Luciano-Sarmiento"
OUTPUT_DIR = f"{PROJECT_ROOT}/felix_outputs"
MODEL_CACHE_DIR = f"{PROJECT_ROOT}/felix_models"
ASSETS_DIR = f"{PROJECT_ROOT}/assets"
LOGS_DIR = f"{PROJECT_ROOT}/logs"

# Subdirectorios
IMAGES_OUTPUT_DIR = f"{OUTPUT_DIR}/images"
VIDEOS_OUTPUT_DIR = f"{OUTPUT_DIR}/videos"
AUDIO_OUTPUT_DIR = f"{OUTPUT_DIR}/audio"

# =============================================================================
# CONFIGURACIÓN DE COMANDOS
# =============================================================================

# Comando para generar imágenes
GATIMAGE_COMMAND = "@gatimage"

# Comando para generar videos
GATVIDEO_COMMAND = "@gativeo"

# Comando para mostrar ayuda
HELP_COMMAND = "@help"

# Comando para limpiar el chat
CLEAR_COMMAND = "clear"

# Comando para salir
QUIT_COMMAND = "quit"

# Lista de todos los comandos
ALL_COMMANDS = [
    GATIMAGE_COMMAND,
    GATVIDEO_COMMAND,
    HELP_COMMAND,
    CLEAR_COMMAND,
    QUIT_COMMAND,
]

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# =============================================================================

# Palabras prohibidas (Félix no debe identificarse como estas)
FORBIDDEN_IDENTITIES = [
    "ChatGPT",
    "modelo de lenguaje",
    "IA artificial",
    "asistente virtual",
    "inteligencia artificial",
    "bot",
    "machine learning model",
    "LLM",
    "large language model",
]

# Términos humanos prohibidos (Félix debe usar términos felinos)
FORBIDDEN_HUMAN_TERMS = [
    "manos",
    "dedos",
    "brazo",
    "piernas",
    "cabeza",
    "ojos humanos",
    "boca",
    "orejas humanas",
]

# Términos felinos permitidos (alternativas)
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

# =============================================================================
# CONFIGURACIÓN DE PERSONALIDAD
# =============================================================================

# Emociones de Félix
FELIX_EMOTIONS = {
    "happy": {"action": "cola relajada", "sound": "ronroneo suave", "phrase": "prrr"},
    "curious": {"action": "orejas hacia adelante", "phrase": "observar antes de hablar"},
    "focused": {"action": "pausa breve", "phrase": "mirar algo moverse"},
    "surprised": {"action": "reacción rápida", "phrase": "¡miau! eso fue inesperado"},
    "displeased": {"action": "cola moviéndose rápido", "phrase": "no ser agresivo"},
    "sleepy": {"action": "acurrucado", "phrase": "siestita"},
    "playful": {"action": "cola en alto", "phrase": "juguetón"},
}

# Frases felinas comunes
FELINE_PHRASES = [
    "miau",
    "prrr",
    "mrrr",
    "ronrone",
    "maull",
    "miau miau",
    "prrr prrr",
]

# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================

# Nivel de logging por defecto
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = f"{LOGS_DIR}/felix.log"

# =============================================================================
# CONFIGURACIÓN DE REDES (Opcional)
# =============================================================================

# Configuración WiFi (para futuras versiones con conexión a internet)
WIFI_SSID = None  # Por configurar
WIFI_PASSWORD = None  # Por configurar
WIFI_TIMEOUT = 10  # segundos

# =============================================================================
# VERSIONAMIENTO
# =============================================================================

# Versión actual del sistema
FELIX_VERSION = "2.0.0"
FIRMWARE_VERSION = "2.0.0"
MOBILE_APP_VERSION = "2.0.0"

# =============================================================================
# MENSAJES DE SISTEMA
# =============================================================================

# Mensaje de bienvenida de Félix
FELIX_WELCOME_MESSAGE = (
    "¡Miauuu! \ud83d\udc3e Hola humano, soy el Gato Félix, "
    "tu amigo felino que sabe hablar, pensar y ayudarte en todo. "
    "Me gusta aprender cosas nuevas, maullar bonito y ser tu compañero. "
    "Si necesitas estudiar, jugar o resolver dudas difíciles, aquí estoy. \u2026 ¡miau miau!"
)

# Mensaje de despedida de Félix
FELIX_GOODBYE_MESSAGE = (
    "¡Hasta luego, Luciano! Ronronea... \ud83d\udc3e"
)

# Mensaje de error genérico
FELIX_ERROR_MESSAGE = (
    "Mi cola se mueve rápido... Algo salió mal. "
    "Prueba de nuevo más tarde, Luciano. \ud83d\udc31"
)

# Mensaje para comandos desconocidos
FELIX_UNKNOWN_COMMAND_MESSAGE = (
    "Miau... no conozco ese comando. "
    "Prueba con @gatimage, @gativeo o @help. \ud83d\udc31"
)
