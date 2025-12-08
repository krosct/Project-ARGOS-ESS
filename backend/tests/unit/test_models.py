"""
Testes unitários para os modelos SQLAlchemy.
Testa a estrutura e comportamento dos modelos de dados.
"""
import pytest
from sqlalchemy import String, Text, DateTime as SA_DateTime

from app.models import CheckRecord


class TestCheckRecordModel:
    """Testes para o modelo CheckRecord"""

    def test_check_record_tablename(self):
        """Verifica se o nome da tabela está correto"""
        assert CheckRecord.__tablename__ == "checks"

    def test_check_record_columns_exist(self):
        """Verifica se todas as colunas necessárias existem"""
        required_columns = [
            'id',
            'text',
            'status',
            'result',
            'created_at'
        ]

        for col in required_columns:
            assert hasattr(CheckRecord, col), (
                f"Coluna '{col}' não encontrada"
            )

    def test_check_record_id_is_primary_key(self):
        """Verifica se 'id' é chave primária"""
        id_column = CheckRecord.__table__.columns['id']

        assert id_column.primary_key is True
        assert id_column.index is True

    def test_check_record_text_not_nullable(self):
        """Verifica se 'text' não aceita NULL"""
        text_column = CheckRecord.__table__.columns['text']

        assert text_column.nullable is False

    def test_check_record_status_default_value(self):
        """Verifica se 'status' tem valor padrão correto"""
        status_column = CheckRecord.__table__.columns['status']

        assert status_column.default.arg == "ANALYSING"

    def test_check_record_result_nullable(self):
        """Verifica se 'result' aceita NULL"""
        result_column = CheckRecord.__table__.columns['result']

        assert result_column.nullable is True

    def test_check_record_created_at_has_default(self):
        """Verifica se 'created_at' tem valor padrão (func.now())"""
        created_at_column = CheckRecord.__table__.columns['created_at']

        assert created_at_column.server_default is not None

    def test_check_record_created_at_is_datetime(self):
        """Verifica se 'created_at' é do tipo DateTime"""
        created_at_column = CheckRecord.__table__.columns['created_at']

        assert isinstance(created_at_column.type, SA_DateTime)

    def test_check_record_column_types(self):
        """Verifica os tipos de cada coluna"""
        columns = CheckRecord.__table__.columns

        assert isinstance(columns['id'].type, String)
        assert isinstance(columns['text'].type, Text)
        assert isinstance(columns['status'].type, String)
        assert isinstance(columns['result'].type, String)
        assert isinstance(columns['created_at'].type, SA_DateTime)

    def test_check_record_instantiation(self):
        """
        Testa criação de instância do modelo.
        Não persiste no banco de dados.
        """
        check = CheckRecord(
            id="test-uuid-123",
            text="Notícia de teste",
            status="ANALYSING",
            result=None
        )

        assert check.id == "test-uuid-123"
        assert check.text == "Notícia de teste"
        assert check.status == "ANALYSING"
        assert check.result is None

    def test_check_record_with_result(self):
        """Testa criação com resultado já definido"""
        check = CheckRecord(
            id="test-uuid-456",
            text="Texto analisado",
            status="COMPLETED",
            result="Fake News detectada"
        )

        assert check.status == "COMPLETED"
        assert check.result == "Fake News detectada"

    def test_check_record_repr_exists(self):
        """Verifica se o modelo pode ser representado como string"""
        check = CheckRecord(
            id="test-uuid-789",
            text="Teste",
            status="ANALYSING"
        )

        repr_str = str(check)
        assert isinstance(repr_str, str)