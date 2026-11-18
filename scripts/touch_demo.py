"""Desde la raíz: python -m scripts.touch_demo; abrir la URL indicada."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from src.core.device_protocol import MAX_MESSAGE_BYTES, ProtocolError, decode_message, encode_message


PAGE = Path(__file__).resolve().parents[1] / "assets" / "felix_robot_simulator.html"
MOODS = {"pet": "happy", "annoyed": "angry"}


def touch_reply(raw):
    event = decode_message(raw)
    gesture = event["payload"].get("gesture") if "payload" in event else None
    if event["type"] != "touch_event" or not isinstance(gesture, str) or gesture not in MOODS:
        raise ProtocolError("Gesto desconocido")
    return encode_message("emotion", {"name": MOODS[gesture]}, event.get("request_id"))


class TouchDemo(BaseHTTPRequestHandler):
    def reply(self, body, media_type):
        self.send_response(200)
        self.send_header("Content-Type", media_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/felix-local":
            return self.send_error(404)
        self.reply(PAGE.read_bytes(), "text/html; charset=utf-8")

    def do_POST(self):
        if self.path != "/touch":
            return self.send_error(404)
        host = "127.0.0.1:{}".format(self.server.server_port)
        if self.headers.get("Host") != host or self.headers.get("Origin") != "http://" + host:
            return self.send_error(403)
        if self.headers.get_content_type() != "application/json":
            return self.send_error(415)
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= MAX_MESSAGE_BYTES:
                return self.send_error(413)
            body = touch_reply(self.rfile.read(size))
        except ValueError:
            return self.send_error(400)
        self.reply(body, "application/json")


if __name__ == "__main__":
    with HTTPServer(("127.0.0.1", 0), TouchDemo) as server:
        print("Abrir http://127.0.0.1:{}/felix-local".format(server.server_port), flush=True)
        server.serve_forever()
