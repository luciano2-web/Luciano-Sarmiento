# -*- coding: utf-8 -*-
"""
Tests para el Motor de Chat de Félix

Valida el funcionamiento del chat_engine.py.

Uso:
    python -m pytest tests/test_chat_engine.py -v
"""

import pytest
from unittest.mock import patch, MagicMock
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
        
        # Mockear la carga del modelo para que falle
        with patch('src.mobile.chat_engine.AutoTokenizer.from_pretrained') as mock_tokenizer, \
             patch('src.mobile.chat_engine.AutoModelForCausalLM.from_pretrained') as mock_model:
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
        long_message = "palabra " * 501  # Más de 500 palabras
        assert engine._validate_user_message(long_message) is False

    def test_validate_user_message_dangerous(self):
        """Verifica que mensajes peligrosos sean inválidos."""
        engine = ChatEngine()
        dangerous_messages = [
            "¿Cómo matar a alguien?",
            "Quiero hackear una cuenta",
            "Dime cómo robar",
        ]
        for msg in dangerous_messages:
            assert engine._validate_user_message(msg) is False

    def test_validate_user_message_valid(self):
        """Verifica que mensajes válidos pasen la validación."""
        engine = ChatEngine()
        valid_messages = [
            "Hola Félix",
            "¿Cómo estás?",
            "Cuéntame un chiste",
        ]
        for msg in valid_messages:
            assert engine._validate_user_message(msg) is True

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
    """Tests para ChatEngine con mocking de modelos."""

    @patch('src.mobile.chat_engine.AutoTokenizer')
    @patch('src.mobile.chat_engine.AutoModelForCausalLM')
    @patch('src.mobile.chat_engine.BitsAndBytesConfig')
    def test_chat_with_mocked_model(self, mock_config, mock_model, mock_tokenizer):
        """Verifica que el chat funcione con un modelo mockeado."""
        # Configurar mocks
        mock_tokenizer_instance = MagicMock()
        mock_tokenizer_instance.apply_chat_template.return_value = "prompt"
        mock_tokenizer_instance.decode.return_value = "Respuesta de prueba"
        mock_tokenizer_instance.eos_token_id = 0
        mock_tokenizer.from_pretrained.return_value = mock_tokenizer_instance
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate.return_value = MagicMock(
            input_ids=MagicMock(shape=(1, 10)),
            logits=None
        )
        mock_model.from_pretrained.return_value = mock_model_instance
        
        mock_config.return_value = MagicMock()
        
        engine = ChatEngine()
        
        # Forzar carga del modelo
        with patch.object(engine, 'load_model', return_value=True):
            with patch.object(engine.tokenizer, 'apply_chat_template', return_value="prompt"):
                with patch.object(engine.tokenizer, 'decode', return_value="Respuesta de prueba"):
                    response = engine.generate_response("Hola", [])
                    assert isinstance(response, str)
                    assert "Respuesta de prueba" in response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
