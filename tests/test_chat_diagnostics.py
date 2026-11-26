"""Offline regressions for input handling and model failure diagnostics."""
import unittest
from unittest.mock import patch
from src.mobile.chat_engine import ChatEngine


class ChatDiagnosticsTests(unittest.TestCase):
    def test_ordinary_questions_are_not_rejected_by_substrings(self):
        engine = ChatEngine()
        for text in ('¿Cómo funciona una alarma?', 'Quiero armar un robot',
                     '¿Cómo prevenir la violencia?'):
            with self.subTest(text=text), patch.object(engine, 'load_model', return_value=False) as load:
                result = engine.generate_response(text)
                load.assert_called_once()
                self.assertIn('IA no disponible', result)
        self.assertFalse(engine._validate_user_message(' '))
        self.assertFalse(engine._validate_user_message('hola ' * 501))

    def test_missing_packages_are_identified_without_network(self):
        engine = ChatEngine()
        with patch('src.mobile.chat_engine.AutoTokenizer', None):
            result = engine.generate_response('Hola')
        self.assertIn('Faltan dependencias', result)
        self.assertIn('no una respuesta generada', result)
        self.assertNotIn('más simple', result)
        self.assertFalse(engine.is_loaded)

    def test_inference_error_is_reported(self):
        engine = ChatEngine()
        with patch.object(engine, 'load_model', return_value=True):
            result = engine.generate_response('Hola')
        self.assertIn('IA no disponible', result)
        self.assertIn('AttributeError', engine.last_error)


if __name__ == '__main__':
    unittest.main()
