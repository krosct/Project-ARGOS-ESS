"""
Testes unitários para o router de autenticação.
Testa as rotas de login isoladamente (sem banco de dados).
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAuthRouter:
    """Testes para as rotas de autenticação"""

    def test_login_endpoint_exists(self):
        """Verifica se o endpoint /api/auth/login existe"""
        response = client.post(
            "/api/auth/login",
            json={"username": "test", "password": "test"}
        )

        assert response.status_code != 404

    def test_login_success(self):
        """Testa login bem-sucedido com credenciais válidas"""
        response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "testpass123"}
        )

        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_login_returns_token(self):
        """Verifica se o login retorna um token válido"""
        response = client.post(
            "/api/auth/login",
            json={"username": "user", "password": "pass"}
        )

        data = response.json()
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0

    def test_login_with_empty_username(self):
        """Testa login com username vazio"""
        response = client.post(
            "/api/auth/login",
            json={"username": "", "password": "password"}
        )

        # Pydantic aceita, validação de negócio deve ser na rota
        assert response.status_code == 200

    def test_login_with_empty_password(self):
        """Testa login com senha vazia"""
        response = client.post(
            "/api/auth/login",
            json={"username": "user", "password": ""}
        )

        assert response.status_code == 200

    def test_login_missing_username(self):
        """Testa login sem campo username"""
        response = client.post(
            "/api/auth/login",
            json={"password": "password"}
        )

        assert response.status_code == 422

    def test_login_missing_password(self):
        """Testa login sem campo password"""
        response = client.post(
            "/api/auth/login",
            json={"username": "user"}
        )

        assert response.status_code == 422

    def test_login_invalid_json(self):
        """Testa login com JSON inválido"""
        response = client.post(
            "/api/auth/login",
            data="invalid json"
        )

        assert response.status_code == 422

    def test_login_extra_fields(self):
        """Testa login com campos extras (devem ser ignorados)"""
        response = client.post(
            "/api/auth/login",
            json={
                "username": "user",
                "password": "pass",
                "extra_field": "should be ignored"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "extra_field" not in data

    def test_login_special_characters_in_username(self):
        """Testa login com caracteres especiais no username"""
        response = client.post(
            "/api/auth/login",
            json={"username": "user@domain.com", "password": "pass123"}
        )

        assert response.status_code == 200

    def test_login_unicode_characters(self):
        """Testa login com caracteres unicode"""
        response = client.post(
            "/api/auth/login",
            json={"username": "usuário_tëst", "password": "señá123"}
        )

        assert response.status_code == 200

    def test_login_response_structure(self):
        """Verifica estrutura completa da resposta"""
        response = client.post(
            "/api/auth/login",
            json={"username": "test", "password": "test"}
        )

        data = response.json()

        assert len(data) == 2
        assert "access_token" in data
        assert "token_type" in data

    def test_login_method_not_allowed(self):
        """Testa que GET não é permitido em /login"""
        response = client.get("/api/auth/login")

        assert response.status_code == 405

    def test_login_content_type(self):
        """Verifica que a resposta tem Content-Type correto"""
        response = client.post(
            "/api/auth/login",
            json={"username": "test", "password": "test"}
        )

        assert "application/json" in response.headers["content-type"]