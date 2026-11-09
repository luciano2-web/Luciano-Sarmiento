"""Pruebas de la lógica de eventos del sensor capacitivo."""

import unittest

from src.firmware.touch_sensor import TouchSensor


class FakeTouchPad:
    def __init__(self, values):
        self.values = iter(values)
        self.last = 1000

    def read(self):
        try:
            self.last = next(self.values)
        except StopIteration:
            pass
        return self.last


class TouchSensorTests(unittest.TestCase):
    def test_short_touch_emits_pet_on_release(self):
        pad = FakeTouchPad([1000, 500, 500, 1000, 1000])
        sensor = TouchSensor(pad, threshold=800, debounce_ms=0)
        self.assertIsNone(sensor.poll(0))
        self.assertIsNone(sensor.poll(10))  # comienza el debounce
        self.assertEqual(sensor.poll(11)["type"], "touch_start")
        self.assertIsNone(sensor.poll(100))  # se inicia la liberación
        self.assertEqual(sensor.poll(101)["type"], "pet")

    def test_long_touch_emits_press_to_talk_events(self):
        pad = FakeTouchPad([1000, 500, 500, 500, 1000, 1000])
        sensor = TouchSensor(
            pad, threshold=800, long_press_ms=900, debounce_ms=0
        )
        self.assertIsNone(sensor.poll(0))
        self.assertIsNone(sensor.poll(10))
        self.assertEqual(sensor.poll(11)["type"], "touch_start")
        self.assertIsNone(sensor.poll(500))
        self.assertEqual(sensor.poll(911)["type"], "press_to_talk_start")
        self.assertIsNone(sensor.poll(920))  # comienza la liberación
        self.assertEqual(sensor.poll(921)["type"], "press_to_talk_end")


if __name__ == "__main__":
    unittest.main()
