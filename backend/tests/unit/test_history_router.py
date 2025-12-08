"""
Testes unitários para o router de histórico.
Testa a rota de consulta do histórico de análises.
Utiliza mocks do Supabase para isolamento.
"""
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_supabase():
    """Mock do cliente Supabase para testes unitários"""
    with patch("app.routers.history.supabase") as mock:
        yield mock


class TestHistoryRouter:
    """Testes para a rota de histórico"""

    def test_history_endpoint_exists(self, mock_supabase):
        """Verifica se o endpoint GET /api/history existe"""
        mock_response = MagicMock()
        mock_response.data = []
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        assert response.status_code != 404

    def test_get_history_success(self, mock_supabase):
        """Testa consulta bem-sucedida do histórico"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": "Notícia sobre eleições",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        assert response.status_code == 200

    def test_get_history_returns_list(self, mock_supabase):
        """Verifica se retorna uma lista"""
        mock_response = MagicMock()
        mock_response.data = []
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()
        assert isinstance(data, list)

    def test_get_history_items_structure(self, mock_supabase):
        """Verifica estrutura dos itens do histórico"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": "Notícia sobre eleições presidenciais",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        if len(data) > 0:
            item = data[0]
            required_fields = [
                "id",
                "text_preview",
                "date",
                "status"
            ]

            for field in required_fields:
                assert field in item, (
                    f"Campo '{field}' não encontrado"
                )

    def test_get_history_returns_multiple_items(self, mock_supabase):
        """Verifica se retorna múltiplos itens"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": "Texto 1",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            },
            {
                "id": "2",
                "text": "Texto 2",
                "status": "FAKE",
                "created_at": "2023-10-28T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()
        assert len(data) == 2

    def test_get_history_item_has_valid_id(self, mock_supabase):
        """Verifica se cada item tem ID válido"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "test-id-123",
                "text": "Texto",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        for item in data:
            assert "id" in item
            assert isinstance(item["id"], str)
            assert len(item["id"]) > 0

    def test_get_history_item_has_text_preview(self, mock_supabase):
        """Verifica se cada item tem preview de texto"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": "Este é um texto de exemplo",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        for item in data:
            assert "text_preview" in item
            assert isinstance(item["text_preview"], str)

    def test_get_history_item_has_date(self, mock_supabase):
        """Verifica se cada item tem data"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": "Texto",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        for item in data:
            assert "date" in item
            assert isinstance(item["date"], str)

    def test_get_history_item_has_status(self, mock_supabase):
        """Verifica se cada item tem status"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": "Texto",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        for item in data:
            assert "status" in item
            assert isinstance(item["status"], str)

    def test_get_history_date_format(self, mock_supabase):
        """Verifica formato das datas (YYYY-MM-DD)"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": "Texto",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        for item in data:
            date_str = item["date"]
            parts = date_str.split("-")
            assert len(parts) == 3
            assert len(parts[0]) == 4  # ano
            assert len(parts[1]) == 2  # mês
            assert len(parts[2]) == 2  # dia

    def test_get_history_text_preview_truncation(self, mock_supabase):
        """Verifica se textos longos são truncados"""
        long_text = "A" * 100
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": long_text,
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        for item in data:
            # Preview deve ser truncado (60 chars + "...")
            assert len(item["text_preview"]) <= 63

    def test_get_history_database_error(self, mock_supabase):
        """Testa tratamento de erro do banco de dados"""
        mock_response = MagicMock()
        mock_response.data = None
        mock_response.error = {"message": "Connection failed"}
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        assert response.status_code == 503
        assert "Database unavailable" in response.json()["detail"]

    def test_get_history_different_statuses(self, mock_supabase):
        """Verifica se há itens com status diferentes"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": "Texto 1",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            },
            {
                "id": "2",
                "text": "Texto 2",
                "status": "FAKE",
                "created_at": "2023-10-28T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        if len(data) >= 2:
            statuses = [item["status"] for item in data]
            assert len(set(statuses)) > 1

    def test_get_history_method_not_allowed(self):
        """Testa que POST não é permitido"""
        response = client.post("/api/history/")

        assert response.status_code == 405

    def test_get_history_content_type(self, mock_supabase):
        """Verifica Content-Type da resposta"""
        mock_response = MagicMock()
        mock_response.data = []
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        content_type = response.headers["content-type"]
        assert "application/json" in content_type

    def test_get_history_empty_response_is_valid(self, mock_supabase):
        """Verifica que lista vazia é uma resposta válida"""
        mock_response = MagicMock()
        mock_response.data = []
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_history_ordered_by_date(self, mock_supabase):
        """Verifica se itens são ordenados por data (mais recente primeiro)"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "2",
                "text": "Texto recente",
                "status": "VERIFIED",
                "created_at": "2023-10-28T10:00:00"
            },
            {
                "id": "1",
                "text": "Texto antigo",
                "status": "FAKE",
                "created_at": "2023-10-27T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        if len(data) >= 2:
            # Primeiro item deve ser mais recente
            assert data[0]["date"] >= data[1]["date"]


class TestHistoryItemValidation:
    """Testes de validação dos campos dos itens"""

    def test_history_text_preview_not_empty(self, mock_supabase):
        """Verifica se text_preview não está vazio"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": "Texto válido",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        for item in data:
            assert len(item["text_preview"]) > 0

    def test_history_id_uniqueness(self, mock_supabase):
        """Verifica se os IDs são únicos"""
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "text": "Texto 1",
                "status": "VERIFIED",
                "created_at": "2023-10-27T10:00:00"
            },
            {
                "id": "2",
                "text": "Texto 2",
                "status": "FAKE",
                "created_at": "2023-10-28T10:00:00"
            }
        ]
        mock_response.error = None
        mock_supabase.table().select().order().limit().execute.return_value = (  # noqa: E501
            mock_response
        )

        response = client.get("/api/history/")

        data = response.json()

        ids = [item["id"] for item in data]
        assert len(ids) == len(set(ids)), (
            "IDs duplicados encontrados"
        )