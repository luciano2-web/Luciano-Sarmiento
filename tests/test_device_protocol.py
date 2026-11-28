import unittest

from src.core.device_protocol import (
    MAX_MESSAGE_BYTES, ProtocolError, decode_message, encode_message
)
from tests.simulated_link import SimulatedLink


class DeviceProtocolTests(unittest.TestCase):
    def test_jsonl_round_trip_keeps_spanish_text(self):
        message = decode_message(encode_message(
            "assistant_text", {"text": "¡Hola! ¿Cómo estás, Luciano?"},
            request_id="r-1"
        ))
        self.assertEqual(message["payload"]["text"], "¡Hola! ¿Cómo estás, Luciano?")
        self.assertEqual(message["request_id"], "r-1")

    def test_jsonl_size_limit_excludes_line_feed(self):
        overhead = len(encode_message("assistant_text", {"text": ""})) - 1
        for body_size in (MAX_MESSAGE_BYTES - 1, MAX_MESSAGE_BYTES):
            payload = {"text": "a" * (body_size - overhead)}
            with self.subTest(body_size=body_size):
                frame = encode_message("assistant_text", payload)
                self.assertEqual(len(frame), body_size + 1)
                self.assertEqual(decode_message(frame)["payload"], payload)
                self.assertEqual(decode_message(frame[:-1])["payload"], payload)

        payload = {"text": "a" * (MAX_MESSAGE_BYTES + 1 - overhead)}
        with self.assertRaises(ProtocolError):
            encode_message("assistant_text", payload)
        frame = encode_message("assistant_text", {"text": payload["text"][:-1]})
        with self.assertRaises(ProtocolError):
            decode_message(frame[:-2] + b" \n")

    def test_rejects_unknown_type(self):
        with self.assertRaises(ProtocolError):
            encode_message("execute_shell", {})

    def test_rejects_wrong_version(self):
        with self.assertRaises(ProtocolError):
            decode_message(b'{"version":99,"type":"ping","payload":{}}')

    def test_simulated_app_robot_round_trip(self):
        link = SimulatedLink()
        link.app_send("hello", {"device":"tablet"})
        request = link.robot_receive()
        self.assertEqual(request["type"], "hello")
        link.robot_send("hello_ack", {"device":"Felix ESP32"})
        reply = link.app_receive()
        self.assertEqual(reply["payload"]["device"], "Felix ESP32")

    def test_simulation_disconnect_is_not_connected(self):
        link = SimulatedLink()
        link.disconnect()
        with self.assertRaises(ConnectionError):
            link.app_send("ping")


if __name__ == "__main__":
    unittest.main()
