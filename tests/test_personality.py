# -*- coding: utf-8 -*-
"""
Tests para el Sistema de Personalidad de Félix

Valida que el sistema de personalidad de Félix funcione correctamente
en todas las versiones (Mobile, Colab, etc.).

Uso:
    python -m pytest tests/test_personality.py -v
"""

import pytest
from src.core.personality import (
    FELIX_SYSTEM_PROMPT,
    FELIX_SYSTEM_PROMPT_MOBILE,
    FELIX_PERSONALITY_RULES,
    validate_felix_response,
)


class TestPersonalityRules:
    """Tests para las reglas de personalidad de Félix."""

    def test_felix_system_prompt_exists(self):
        """Verifica que el prompt del sistema existe."""
        assert FELIX_SYSTEM_PROMPT is not None
        assert len(FELIX_SYSTEM_PROMPT) > 0

    def test_felix_system_prompt_mobile_exists(self):
        """Verifica que el prompt móvil existe."""
        assert FELIX_SYSTEM_PROMPT_MOBILE is not None
        assert len(FELIX_SYSTEM_PROMPT_MOBILE) > 0

    def test_felix_personality_rules_structure(self):
        """Verifica la estructura de las reglas de personalidad."""
        assert isinstance(FELIX_PERSONALITY_RULES, dict)
        assert "identity" in FELIX_PERSONALITY_RULES
        assert "behavior" in FELIX_PERSONALITY_RULES
        assert "speech" in FELIX_PERSONALITY_RULES
        assert "commands" in FELIX_PERSONALITY_RULES
        assert "safety" in FELIX_PERSONALITY_RULES

    def test_felix_identity(self):
        """Verifica la identidad de Félix."""
        identity = FELIX_PERSONALITY_RULES["identity"]
        assert identity["name"] == "Félix"
        assert identity["alias"] == "GatoGPT"
        assert identity["creator"] == "Luciano"

    def test_felix_forbidden_identities(self):
        """Verifica que Félix no se identifique como IA."""
        identity = FELIX_PERSONALITY_RULES["identity"]
        forbidden = identity["forbidden_identities"]
        assert "ChatGPT" in forbidden
        assert "modelo de lenguaje" in forbidden
        assert "IA artificial" in forbidden

    def test_felix_behavior_rules(self):
        """Verifica las reglas de comportamiento de Félix."""
        behavior = FELIX_PERSONALITY_RULES["behavior"]
        assert "happy" in behavior
        assert "curious" in behavior
        assert "focused" in behavior
        assert "surprised" in behavior
        assert "displeased" in behavior


class TestValidateFelixResponse:
    """Tests para la función validate_felix_response."""

    def test_valid_response(self):
        """Verifica que una respuesta válida pase la validación."""
        response = "🐱 Hola Luciano, soy Félix, tu amigo felino. ¿En qué puedo ayudarte?"
        is_valid, issues, suggestions = validate_felix_response(response)
        assert is_valid is True
        assert len(issues) == 0

    def test_valid_mobile_response(self):
        """Verifica que una respuesta válida para móvil pase la validación."""
        response = "🐱 Miau! Estoy aquí."
        is_valid, issues, suggestions = validate_felix_response(response, is_mobile=True)
        assert is_valid is True

    def test_too_long_response(self):
        """Verifica que una respuesta demasiado larga falle."""
        # Crear una respuesta con más de 450 palabras
        long_response = "🐱 " + "palabra " * 451
        is_valid, issues, suggestions = validate_felix_response(long_response, is_mobile=False)
        assert is_valid is False
        assert any("Respuesta demasiado larga" in issue for issue in issues)

    def test_too_long_mobile_response(self):
        """Verifica que una respuesta móvil demasiado larga falle."""
        # Crear una respuesta con más de 100 palabras
        long_response = "🐱 " + "palabra " * 101
        is_valid, issues, suggestions = validate_felix_response(long_response, is_mobile=True)
        assert is_valid is False
        assert any("Respuesta demasiado larga" in issue for issue in issues)

    def test_too_many_feline_phrases(self):
        """Verifica que demasiadas frases felinas fallen."""
        response = "🐱 miau miau miau prrr prrr mrrr"
        is_valid, issues, suggestions = validate_felix_response(response)
        assert is_valid is False
        assert any("Demasiadas frases felinas" in issue for issue in issues)

    def test_forbidden_identity(self):
        """Verifica que Félix no se identifique como ChatGPT."""
        response = "Hola, soy ChatGPT, un modelo de lenguaje."
        is_valid, issues, suggestions = validate_felix_response(response)
        assert is_valid is False
        assert any("Identificación prohibida" in issue for issue in issues)

    def test_human_terms(self):
        """Verifica que Félix no use términos humanos."""
        response = "🐱 Voy a usar mis manos para ayudarte."
        is_valid, issues, suggestions = validate_felix_response(response)
        assert is_valid is False
        assert any("Término humano" in issue for issue in issues)

    def test_missing_feline_personality(self):
        """Verifica que una respuesta sin personalidad felina falle."""
        response = "Hola, ¿en qué puedo ayudarte?"
        is_valid, issues, suggestions = validate_felix_response(response)
        assert is_valid is False
        assert any("Falta personalidad felina" in issue for issue in issues)

    def test_valid_feline_terms(self):
        """Verifica que los términos felinos sean aceptados."""
        response = "🐱 Con mis patitas y bigotes, te ayudo."
        is_valid, issues, suggestions = validate_felix_response(response)
        assert is_valid is True


class TestResponseCorrection:
    """Tests para la corrección de respuestas."""

    def test_add_feline_personality(self):
        """Verifica que se añada personalidad felina si falta."""
        response = "Hola, ¿en qué puedo ayudarte?"
        is_valid, issues, suggestions = validate_felix_response(response)
        assert not is_valid
        assert any("Falta personalidad felina" in issue for issue in issues)

    def test_limit_feline_phrases(self):
        """Verifica que se limiten las frases felinas."""
        response = "🐱 miau miau miau prrr prrr"
        is_valid, issues, suggestions = validate_felix_response(response)
        assert not is_valid
        assert any("Demasiadas frases felinas" in issue for issue in issues)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
