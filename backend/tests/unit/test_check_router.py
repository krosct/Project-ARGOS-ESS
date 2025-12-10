"""
Testes unitários para o router de verificação de fake news.
Testa as rotas de submissão e consulta de análises.
Utiliza mocks do Supabase para isolamento.
"""
import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_supabase():
    """Mock do cliente Supabase para testes unitários"""
    with patch("app.routers.check.supabase") as mock:
        yield mock


class TestCheckSubmission:
    """Testes para submissão de textos para análise"""

    def test_submit_check_endpoint_exists(self, mock_supabase):
        """Verifica se o endpoint POST /api/check existe"""
        mock_response = MagicMock()
        mock_response.data = [{"id": "test-id"}]
        mock_response.error = None
        mock_supabase.table().insert().execute.return_value = (
            mock_response
        )

        response = client.post(
            "/api/check/",
            json={"text": "Notícia teste"}
        )

        assert response.status_code != 404

    def test_submit_check_success(self, mock_supabase):
        """Testa submissão bem-sucedida de texto"""
        mock_response = MagicMock()
        mock_response.data = [{"id": "test-id"}]
        mock_response.error = None
        mock_supabase.table().insert().execute.return_value = (
            mock_response
        )

        response = client.post(
            "/api/check/",
            json={"text": "Notícia sobre as eleições presidenciais"}
        )

        assert response.status_code == 200

        data = response.json()
        assert "id" in data
        assert "status" in data

    def test_submit_check_returns_valid_uuid(self, mock_supabase):
        """Verifica se o ID retornado é um UUID válido"""
        mock_response = MagicMock()
        mock_response.data = [{"id": "test-id"}]
        mock_response.error = None
        mock_supabase.table().insert().execute.return_value = (
            mock_response
        )

        response = client.post(
            "/api/check/",
            json={"text": "Texto qualquer"}
        )

        data = response.json()

        try:
            uuid.UUID(data["id"])
            assert True
        except ValueError:
            pytest.fail("ID retornado não é um UUID válido")

    def test_submit_check_initial_status(self, mock_supabase):
        """Verifica se o status inicial é ANALYSING"""
        mock_response = MagicMock()
        mock_response.data = [{"id": "test-id"}]
        mock_response.error = None
        mock_supabase.table().insert().execute.return_value = (
            mock_response
        )

        response = client.post(
            "/api/check/",
            json={"text": "Notícia de teste"}
        )

        data = response.json()
        assert data["status"] == "ANALYSING"

    def test_submit_check_with_long_text(self, mock_supabase):
        """Testa submissão com texto longo"""
        mock_response = MagicMock()
        mock_response.data = [{"id": "test-id"}]
        mock_response.error = None
        mock_supabase.table().insert().execute.return_value = (
            mock_response
        )

        long_text = "A" * 5000
        response = client.post(
            "/api/check/",
            json={"text": long_text}
        )

        assert response.status_code == 200
        data = response.json()
        assert "id" in data

    def test_submit_check_with_empty_text(self, mock_supabase):
        """Testa submissão com texto vazio (agora validado pelo schema)"""
        mock_response = MagicMock()
        mock_response.data = [{"id": "test-id"}]
        mock_response.error = None
        mock_supabase.table().insert().execute.return_value = mock_response

        response = client.post(
            "/api/check/",
            json={"text": ""}
        )

        # validação do schema impede submissão vazia
        assert response.status_code == 422
        # opcional: verificar detalhe da validação
        detail = response.json().get("detail", [])
        assert isinstance(detail, list)
        assert any(
            d.get("type", "").startswith("string_too_")
            or "at least" in str(d.get("msg", "")).lower()
            for d in detail
        )

    def test_submit_check_with_special_characters(self, mock_supabase):
        """Testa submissão com caracteres especiais"""
        mock_response = MagicMock()
        mock_response.data = [{"id": "test-id"}]
        mock_response.error = None
        mock_supabase.table().insert().execute.return_value = (
            mock_response
        )

        special_text = "Notícia com @#$%&*() e çãõ"
        response = client.post(
            "/api/check/",
            json={"text": special_text}
        )

        assert response.status_code == 200

    def test_submit_check_database_error(self, mock_supabase):
        """Testa tratamento de erro do banco de dados"""
        mock_response = MagicMock()
        mock_response.data = None
        mock_response.error = {"message": "Connection failed"}
        mock_supabase.table().insert().execute.return_value = mock_response

        valid_text = "Texto de teste válido"  # >=10 chars
        response = client.post(
            "/api/check/",
            json={"text": valid_text}
        )

        assert response.status_code == 503
        assert "Database unavailable" in response.json()["detail"]

    def test_submit_check_missing_text_field(self):
        """Testa submissão sem campo 'text'"""
        response = client.post("/api/check/", json={})

        assert response.status_code == 422

    def test_submit_check_wrong_field_name(self):
        """Testa submissão com nome de campo incorreto"""
        response = client.post(
            "/api/check/",
            json={"content": "Notícia"}
        )

        assert response.status_code == 422

    def test_submit_check_response_structure(self, mock_supabase):
        """Verifica estrutura completa da resposta"""
        mock_response = MagicMock()
        mock_response.data = [{"id": "test-id"}]
        mock_response.error = None
        mock_supabase.table().insert().execute.return_value = mock_response

        response = client.post(
            "/api/check/",
            json={"text": "Notícia de teste válida"}
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2
        assert "id" in data
        assert "status" in data

    def test_submit_check_generates_unique_ids(self, mock_supabase):
        """Verifica se IDs gerados são únicos"""
        mock_response = MagicMock()
        mock_response.data = [{"id": "test-id"}]
        mock_response.error = None
        mock_supabase.table().insert().execute.return_value = mock_response

        response1 = client.post(
            "/api/check/",
            json={"text": "Texto de teste válido 1"}
        )
        response2 = client.post(
            "/api/check/",
            json={"text": "Texto de teste válido 2"}
        )

        id1 = response1.json()["id"]
        id2 = response2.json()["id"]

        assert id1 != id2


class TestCheckStatus:
    """Testes para consulta de status de análise"""

    def test_get_check_status_endpoint_exists(self, mock_supabase):
        """Verifica se o endpoint GET /api/check/{id} existe"""
        mock_response = MagicMock()
        mock_response.data = {
            "id": "test-id",
            "status": "COMPLETED",
            "result": "Verificado"
        }
        mock_response.error = None
        mock_supabase.table().select().eq().limit().single().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/check/test-id")

        assert response.status_code != 404

    def test_get_check_status_success(self, mock_supabase):
        """Testa consulta de status bem-sucedida"""
        check_id = "test-uuid-123"
        mock_response = MagicMock()
        mock_response.data = {
            "id": check_id,
            "status": "COMPLETED",
            "result": "Fake News detectada"
        }
        mock_response.error = None
        mock_supabase.table().select().eq().limit().single().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get(f"/api/check/{check_id}")

        assert response.status_code == 200

        data = response.json()
        assert "id" in data
        assert "status" in data
        assert "result" in data

    def test_get_check_status_returns_correct_id(self, mock_supabase):
        """Verifica se o ID retornado é o mesmo consultado"""
        check_id = "my-test-id"
        mock_response = MagicMock()
        mock_response.data = {
            "id": check_id,
            "status": "COMPLETED",
            "result": "Verificado"
        }
        mock_response.error = None
        mock_supabase.table().select().eq().limit().single().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get(f"/api/check/{check_id}")

        data = response.json()
        assert data["id"] == check_id

    def test_get_check_status_not_found(self, mock_supabase):
        """Verifica resposta quando check não existe"""
        mock_response = MagicMock()
        mock_response.data = None
        mock_response.error = {"message": "Not found"}
        mock_response.status_code = 404
        mock_supabase.table().select().eq().limit().single().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/check/nonexistent-id")

        assert response.status_code == 404
        assert "Check not found" in response.json()["detail"]

    def test_get_check_status_database_error(self, mock_supabase):
        """Testa tratamento de erro do banco de dados"""
        mock_response = MagicMock()
        mock_response.data = None
        mock_response.error = {"message": "Connection failed"}
        mock_response.status_code = 500
        mock_supabase.table().select().eq().limit().single().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/check/test-id")

        assert response.status_code == 503

    def test_get_check_status_with_uuid(self, mock_supabase):
        """Testa consulta com UUID válido"""
        valid_uuid = str(uuid.uuid4())
        mock_response = MagicMock()
        mock_response.data = {
            "id": valid_uuid,
            "status": "COMPLETED",
            "result": "Verificado"
        }
        mock_response.error = None
        mock_supabase.table().select().eq().limit().single().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get(f"/api/check/{valid_uuid}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == valid_uuid

    def test_get_check_status_response_structure(self, mock_supabase):
        """Verifica estrutura completa da resposta"""
        mock_response = MagicMock()
        mock_response.data = {
            "id": "test-id",
            "status": "COMPLETED",
            "result": "Fake News"
        }
        mock_response.error = None
        mock_supabase.table().select().eq().limit().single().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/check/test-id")

        data = response.json()

        assert "id" in data
        assert "status" in data
        assert "result" in data
        assert len(data) == 3

    def test_get_check_status_method_not_allowed(self):
        """Testa que POST não é permitido para consulta"""
        response = client.post("/api/check/test-id")

        assert response.status_code == 405

    def test_get_check_status_content_type(self, mock_supabase):
        """Verifica Content-Type da resposta"""
        mock_response = MagicMock()
        mock_response.data = {
            "id": "test-id",
            "status": "COMPLETED",
            "result": "OK"
        }
        mock_response.error = None
        mock_supabase.table().select().eq().limit().single().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/check/test-id")

        content_type = response.headers["content-type"]
        assert "application/json" in content_type


class TestCheckRouterIntegration:
    """Testes de fluxo completo (submit → query)"""

    def test_submit_and_query_flow(self, mock_supabase):
        """Testa fluxo completo de submissão e consulta"""
        test_id = str(uuid.uuid4())

        # Mock para submit
        mock_submit_response = MagicMock()
        mock_submit_response.data = [{"id": test_id}]
        mock_submit_response.error = None

        # Mock para query
        mock_query_response = MagicMock()
        mock_query_response.data = {
            "id": test_id,
            "status": "COMPLETED",
            "result": "Verificado"
        }
        mock_query_response.error = None

        mock_supabase.table().insert().execute.return_value = (
            mock_submit_response
        )
        mock_supabase.table().select().eq().limit().single().execute.return_value = (  # noqa: E501
            mock_query_response
        )

        # Submete análise
        submit_response = client.post(
            "/api/check/",
            json={"text": "Notícia sobre vacinas"}
        )

        assert submit_response.status_code == 200
        check_id = submit_response.json()["id"]

        # Consulta status
        status_response = client.get(f"/api/check/{check_id}")

        assert status_response.status_code == 200
        status_data = status_response.json()
        assert "id" in status_data
