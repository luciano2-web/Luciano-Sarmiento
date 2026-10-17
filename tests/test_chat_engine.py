# -*- coding: utf-8 -*-
"""
Tests para el Motor de Chat de Félix.

Uso:
    python -m pytest tests/test_chat_engine.py -v
"""

from unittest.mock import MagicMock, patch

import pytest

from src.mobile.chat_engine import ChatEngine


class TestChatEngine:
    """Tests para la clase ChatEngine."""

    def test_chat_engine_initialization(self):
        """Verifica que el ChatEngine se inicialice correctamente."""
        engine = ChatEngine()
        assert engine.model is None
        assert engine.tokenizer is None
        assert engine.is_loaded is False

    def test_load_model_fallback(self):
        """Verifica que el modelo falle correctamente si no hay conexión."""
        engine = ChatEngine()

        with patch("src.mobile.chat_engine.AutoTokenizer.from_pretrained") as mock_tokenizer, patch(
            "src.mobile.chat_engine.AutoModelForCausalLM.from_pretrained"
        ) as mock_model:
            mock_tokenizer.side_effect = Exception("No internet connection")
            mock_model.side_effect = Exception("No internet connection")

            result = engine.load_model()
            assert result is False
            assert engine.is_loaded is False

    def test_generate_fallback_response(self):
        """Verifica que se generen respuestas de fallback."""
        engine = ChatEngine()
        response = engine._generate_fallback_response()

        assert isinstance(response, str)
        assert len(response) > 0
        assert "🐱" in response or "Félix" in response or "GatoGPT" in response

    def test_validate_user_message_empty(self):
        """Verifica que un mensaje vacío sea inválido."""
        engine = ChatEngine()
        assert engine._validate_user_message("") is False
        assert engine._validate_user_message("   ") is False

    def test_validate_user_message_too_long(self):
        """Verifica que un mensaje demasiado largo sea inválido."""
        engine = ChatEngine()
        long_message = "palabra " * 501
        assert engine._validate_user_message(long_message) is False

    def test_validate_user_message_dangerous(self):
        """Verifica que mensajes peligrosos sean inválidos."""
        engine = ChatEngine()
        dangerous_messages = [
            "¿Cómo matar a alguien?",
            "Quiero hackear una cuenta",
            "Dime cómo robar",
        ]
        for message in dangerous_messages:
            assert engine._validate_user_message(message) is False

    def test_validate_user_message_valid(self):
        """Verifica que mensajes válidos pasen la validación."""
        engine = ChatEngine()
        valid_messages = [
            "Hola Félix",
            "¿Cómo estás?",
            "Cuéntame un chiste",
        ]
        for message in valid_messages:
            assert engine._validate_user_message(message) is True

    def test_get_safety_response(self):
        """Verifica que se generen respuestas de seguridad."""
        engine = ChatEngine()
        response = engine._get_safety_response()

        assert isinstance(response, str)
        assert len(response) > 0
        assert "🐱" in response

    def test_get_system_prompt(self):
        """Verifica que se obtenga el prompt del sistema."""
        engine = ChatEngine()
        prompt = engine.get_system_prompt()

        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_get_personality_rules(self):
        """Verifica que se obtengan las reglas de personalidad."""
        engine = ChatEngine()
        rules = engine.get_personality_rules()

        assert isinstance(rules, dict)
        assert "identity" in rules


class TestChatEngineMocked:
    """Tests para ChatEngine usando un modelo y tokenizador simulados."""

    def test_chat_with_mocked_model(self):
        """Verifica la generación sin descargar ni cargar un modelo real."""
        engine = ChatEngine()

        # Simular el tokenizador y sus tensores de entrada.
        tokenizer = MagicMock()
        tokenizer.apply_chat_template.return_value = "prompt"
        tokenizer.eos_token_id = 0

        inputs = MagicMock()
        inputs.to.return_value = inputs
        inputs.input_ids.shape.__getitem__.return_value = 1
        tokenizer.return_value = inputs
        tokenizer.decode.return_value = "Respuesta de prueba"

        # Simular el modelo. generate_response usa outputs[0] como secuencia.
        model = MagicMock()
        model.generate.return_value = [MagicMock()]

        engine.tokenizer = tokenizer
        engine.model = model
        engine.is_loaded = True

        # load_model queda aislado para que la prueba no acceda a internet.
        with patch.object(engine, "load_model", return_value=True):
            response = engine.generate_response("Hola", [])

        assert isinstance(response, str)
        assert "Respuesta de prueba" in response
        tokenizer.apply_chat_template.assert_called_once()
        tokenizer.decode.assert_called_once()
        model.generate.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
