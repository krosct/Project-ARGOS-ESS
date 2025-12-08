# backend/tests/conftest.py
"""
Configuração global para os testes do backend.
Define fixtures e configurações compartilhadas.
Garante que variáveis de ambiente essenciais e o path do projeto
estejam configurados antes da importação dos módulos do `app`.
"""

import os
import sys
from pathlib import Path

import pytest

# --- Garantir que a raiz `backend/` esteja no sys.path (import app funciona) ---
ROOT = Path(__file__).resolve().parents[1]  # aponta para backend/
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- Valores padrão para testes (serão usados somente se não estiverem definidos) ---
_DEFAULT_ENV = {
    "DATABASE_URL": "sqlite:///:memory:",
    "SUPABASE_HTTP": "1",
    "SUPABASE_URL": "https://test.supabase.co",
    "SUPABASE_SERVICE_ROLE_KEY": "test-key-12345",
}

# Guardar valores originais para restaurar no fim da sessão
_original_env = {}

# Aplicar defaults imediatamente (no import do conftest), garantindo disponibilidade
for k, v in _DEFAULT_ENV.items():
    if k in os.environ:
        _original_env[k] = os.environ[k]
    else:
        _original_env[k] = None
        os.environ[k] = v


def pytest_sessionfinish(session, exitstatus):
    """
    Restaura variáveis de ambiente originais após a sessão de testes.
    """
    for k, orig in _original_env.items():
        if orig is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = orig


# === Fixtures originais (ajustadas levemente) ===

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """
    Fixture autouse para ajustar ambiente durante a execução dos testes.
    Como já aplicamos defaults no import, aqui só expõe a garantia e
    possibilita cleanup extra caso necessário.
    """
    # já foram aplicados defaults no import
    yield
    # nenhum cleanup adicional necessário (pytest_sessionfinish faz restauração)


@pytest.fixture(scope="function")
def mock_database_url():
    """
    Fixture para mockar DATABASE_URL em testes específicos.
    Útil quando você precisa de uma URL específica para um teste.
    """
    original = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    yield "sqlite:///:memory:"

    # restaurar
    if original is not None:
        os.environ["DATABASE_URL"] = original
    else:
        os.environ.pop("DATABASE_URL", None)


@pytest.fixture(scope="function")
def sample_check_data():
    return {
        "id": "test-uuid-12345",
        "text": "Notícia de teste sobre política",
        "status": "ANALYSING",
        "result": None
    }


@pytest.fixture(scope="function")
def sample_supabase_check_data():
    return {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "text": "Notícia sobre eleições presidenciais",
        "status": "ANALYSING",
        "result": None,
        "created_at": "2023-10-27T10:00:00+00:00"
    }


@pytest.fixture(scope="function")
def sample_history_items():
    return [
        {
            "id": "1",
            "text_preview": "Notícia sobre eleições presidenciais...",
            "date": "2023-10-27",
            "status": "VERIFIED"
        },
        {
            "id": "2",
            "text_preview": "Tweet sobre vacinas e saúde pública...",
            "date": "2023-10-28",
            "status": "FAKE"
        },
        {
            "id": "3",
            "text_preview": "Artigo sobre economia brasileira...",
            "date": "2023-10-29",
            "status": "ANALYSING"
        }
    ]


@pytest.fixture(scope="function")
def sample_supabase_history_data():
    return [
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "text": "Notícia sobre eleições presidenciais",
            "status": "VERIFIED",
            "created_at": "2023-10-27T10:00:00+00:00"
        },
        {
            "id": "550e8400-e29b-41d4-a716-446655440002",
            "text": "Tweet sobre vacinas e saúde pública",
            "status": "FAKE",
            "created_at": "2023-10-28T15:30:00+00:00"
        }
    ]


@pytest.fixture(scope="function")
def sample_login_credentials():
    return {
        "valid": {"username": "testuser", "password": "testpass123"},
        "invalid": {"username": "wronguser", "password": "wrongpass"},
        "empty": {"username": "", "password": ""}
    }


def pytest_configure(config):
    """
    Registra markers customizados para os testes.
    """
    config.addinivalue_line("markers", "unit: marca testes unitários")
    config.addinivalue_line("markers", "integration: marca testes de integração")
    config.addinivalue_line("markers", "slow: marca testes que demoram mais tempo")
    config.addinivalue_line("markers", "smoke: marca testes de smoke (básicos)")
    config.addinivalue_line("markers", "supabase: marca testes que usam Supabase")