"""
Testes unitários para validação dos schemas Pydantic.
Garante que os modelos de entrada/saída estão corretamente definidos.
"""
import pytest
from pydantic import ValidationError

from app.schemas import (
    CheckRequest,
    CheckResponse,
    CheckStatusResponse,
    HistoryItem,
    LoginRequest,
    LoginResponse,
)


class TestAuthSchemas:
    """Testes para schemas de autenticação"""

    def test_login_request_valid(self):
        """Testa criação válida de LoginRequest"""
        data = {"username": "user123", "password": "pass123"}
        request = LoginRequest(**data)

        assert request.username == "user123"
        assert request.password == "pass123"

    def test_login_request_missing_fields(self):
        """Testa que LoginRequest requer username e password"""
        with pytest.raises(ValidationError) as exc:
            LoginRequest(username="user123")

        assert "password" in str(exc.value)

    def test_login_response_valid(self):
        """Testa criação válida de LoginResponse"""
        data = {"access_token": "abc123", "token_type": "bearer"}
        response = LoginResponse(**data)

        assert response.access_token == "abc123"
        assert response.token_type == "bearer"

    def test_login_response_missing_token_type(self):
        """Testa que LoginResponse requer token_type"""
        with pytest.raises(ValidationError):
            LoginResponse(access_token="abc123")


class TestCheckSchemas:
    """Testes para schemas de verificação de fake news"""

    def test_check_request_valid(self):
        """Testa criação válida de CheckRequest"""
        data = {"text": "Notícia sobre eleições"}
        request = CheckRequest(**data)

        assert request.text == "Notícia sobre eleições"

    def test_check_request_empty_text(self):
        """
        Testa que CheckRequest aceita texto vazio.
        Validação de negócio deve ser feita na rota.
        """
        data = {"text": ""}
        request = CheckRequest(**data)

        assert request.text == ""

    def test_check_request_long_text(self):
        """Testa CheckRequest com texto longo"""
        long_text = "A" * 10000
        data = {"text": long_text}
        request = CheckRequest(**data)

        assert len(request.text) == 10000

    def test_check_response_valid(self):
        """Testa criação válida de CheckResponse"""
        data = {"id": "uuid-123", "status": "ANALYSING"}
        response = CheckResponse(**data)

        assert response.id == "uuid-123"
        assert response.status == "ANALYSING"

    def test_check_status_response_with_result(self):
        """Testa CheckStatusResponse com resultado"""
        data = {
            "id": "uuid-456",
            "status": "COMPLETED",
            "result": "Fake News detectada"
        }
        response = CheckStatusResponse(**data)

        assert response.id == "uuid-456"
        assert response.status == "COMPLETED"
        assert response.result == "Fake News detectada"

    def test_check_status_response_without_result(self):
        """
        Testa CheckStatusResponse sem resultado.
        Cenário: análise em andamento.
        """
        data = {"id": "uuid-789", "status": "ANALYSING"}
        response = CheckStatusResponse(**data)

        assert response.id == "uuid-789"
        assert response.status == "ANALYSING"
        assert response.result is None

    def test_check_status_response_various_statuses(self):
        """Testa diferentes valores de status"""
        statuses = ["ANALYSING", "COMPLETED", "FAILED", "PENDING"]

        for status in statuses:
            data = {"id": "test-id", "status": status}
            response = CheckStatusResponse(**data)
            assert response.status == status


class TestHistorySchemas:
    """Testes para schemas de histórico"""

    def test_history_item_valid(self):
        """Testa criação válida de HistoryItem"""
        data = {
            "id": "1",
            "text_preview": "Notícia sobre vacinas...",
            "date": "2023-10-27",
            "status": "VERIFIED"
        }
        item = HistoryItem(**data)

        assert item.id == "1"
        assert item.text_preview == "Notícia sobre vacinas..."
        assert item.date == "2023-10-27"
        assert item.status == "VERIFIED"

    def test_history_item_missing_required_fields(self):
        """Testa que HistoryItem requer todos os campos"""
        with pytest.raises(ValidationError):
            HistoryItem(id="1", text_preview="Preview")

    def test_history_item_various_statuses(self):
        """Testa HistoryItem com diferentes status"""
        statuses = ["VERIFIED", "FAKE", "ANALYSING", "ERROR"]

        for i, status in enumerate(statuses):
            data = {
                "id": str(i),
                "text_preview": f"Preview {i}",
                "date": "2023-10-27",
                "status": status
            }
            item = HistoryItem(**data)
            assert item.status == status

    def test_history_item_long_preview(self):
        """Testa HistoryItem com preview longo"""
        long_preview = "A" * 500
        data = {
            "id": "1",
            "text_preview": long_preview,
            "date": "2023-10-27",
            "status": "VERIFIED"
        }
        item = HistoryItem(**data)

        assert len(item.text_preview) == 500