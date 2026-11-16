"""Pruebas de contrato estático del simulador web de Félix.

Ejecutar con: python -m unittest tests.test_web_simulator_contract -v
Estas pruebas comprueban que la interfaz conserve sus controles y eventos
principales. No sustituyen una prueba interactiva en navegador ni una prueba BLE.
"""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SIMULATOR = ROOT / "assets" / "felix_robot_simulator.html"


class WebSimulatorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = SIMULATOR.read_text(encoding="utf-8")

    def test_virtual_transport_is_explicitly_simulated(self):
        self.assertIn("SIMULATOR", self.html)
        self.assertIn("No activa Bluetooth", self.html)
        self.assertIn("VIRTUAL_ESP32", self.html)

    def test_connection_controls_exist(self):
        for element_id in ("simConnect", "simDisconnect", "simDot", "simConnection"):
            with self.subTest(element_id=element_id):
                self.assertIn(f'id="{element_id}"', self.html)

    def test_protocol_handshake_is_present(self):
        self.assertIn("hello_ack", self.html)
        self.assertIn("firmware: 'felix-sim-1.0'", self.html)

    def test_touch_and_push_to_talk_events_are_present(self):
        for event in ("pet", "annoyed", "ptt_start", "ptt_end"):
            with self.subTest(event=event):
                self.assertIn(f"'{event}'", self.html)

    def test_text_message_path_and_event_log_exist(self):
        self.assertIn("chat_message", self.html)
        self.assertIn('id="simLog"', self.html)
        self.assertIn("role=\"log\"", self.html)

    def test_disconnect_cancels_active_push_to_talk(self):
        self.assertIn("ptt_cancelled_by_disconnect", self.html)


if __name__ == "__main__":
    unittest.main()
