# -*- coding: utf-8 -*-
"""Protocolo JSONL compartido entre la app de Félix y el firmware.

Solo transporta mensajes de control y texto. El audio binario se añadirá
mediante tramas BLE fragmentadas cuando se confirme el MTU del hardware.
Compatible con Python estándar y MicroPython.
"""
import json

PROTOCOL_VERSION = 1
MAX_MESSAGE_BYTES = 4096
ALLOWED_TYPES = (
    "hello", "hello_ack", "ping", "pong", "touch_event",
    "audio_start", "audio_end", "transcript", "assistant_text",
    "tts_start", "tts_end", "emotion", "display_text",
    "diagnostic", "error",
)


class ProtocolError(ValueError):
    """Mensaje inválido o incompatible."""


def encode_message(message_type, payload=None, request_id=None):
    if message_type not in ALLOWED_TYPES:
        raise ProtocolError("Tipo de mensaje no permitido: {}".format(message_type))
    message = {
        "version": PROTOCOL_VERSION,
        "type": message_type,
        "payload": payload or {},
    }
    if request_id is not None:
        message["request_id"] = str(request_id)
    raw = json.dumps(message, separators=(",", ":")).encode("utf-8")
    if len(raw) > MAX_MESSAGE_BYTES:
        raise ProtocolError("Mensaje demasiado grande")
    return raw + b"\n"


def decode_message(raw):
    if isinstance(raw, str):
        raw = raw.encode("utf-8")
    if not raw or len(raw) > MAX_MESSAGE_BYTES:
        raise ProtocolError("Tamaño de mensaje inválido")
    try:
        message = json.loads(raw.decode("utf-8").strip())
    except (ValueError, UnicodeError) as exc:
        raise ProtocolError("JSON inválido") from exc
    if not isinstance(message, dict):
        raise ProtocolError("El mensaje debe ser un objeto")
    if message.get("version") != PROTOCOL_VERSION:
        raise ProtocolError("Versión de protocolo incompatible")
    if message.get("type") not in ALLOWED_TYPES:
        raise ProtocolError("Tipo de mensaje desconocido")
    if not isinstance(message.get("payload", {}), dict):
        raise ProtocolError("payload debe ser un objeto")
    return message
