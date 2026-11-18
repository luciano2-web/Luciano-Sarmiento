"""Procesa gestos táctiles de Félix para la app y el simulador."""
from src.core.device_protocol import ProtocolError, decode_message, encode_message


MOODS = {"pet": "happy", "annoyed": "angry"}


def touch_reply(raw):
    event = decode_message(raw)
    gesture = event["payload"].get("gesture") if "payload" in event else None
    if event["type"] != "touch_event" or not isinstance(gesture, str) or gesture not in MOODS:
        raise ProtocolError("Gesto desconocido")
    return encode_message("emotion", {"name": MOODS[gesture]}, event.get("request_id"))
