# Testes Backend - Projeto Argos

## Estrutura de Testes

```
backend/tests/
├── unit/                      # Testes unitários
│   ├── test_schemas.py       # Validação dos schemas Pydantic
│   ├── test_models.py        # Validação dos modelos SQLAlchemy
│   ├── test_auth_router.py   # Testes do router de autenticação
│   ├── test_check_router.py  # Testes do router de verificação (com mocks Supabase)
│   └── test_history_router.py # Testes do router de histórico (com mocks Supabase)
├── integration/              # Testes de integração (próxima etapa)
├── conftest.py              # Configurações e fixtures compartilhadas
└── pytest.ini               # Configurações do pytest
```

## ⚠️ Mudanças Recentes - Integração com Supabase

Os routers `check.py` e `history.py` agora usam **Supabase** ao invés de dados fake. Os testes unitários foram atualizados para:

- ✅ **Mockar o cliente Supabase** usando `unittest.mock`
- ✅ **Isolar os testes** sem dependências externas
- ✅ **Testar tratamento de erros** do banco de dados
- ✅ **Manter 100% de cobertura** dos casos de uso

## Configuração Inicial

### 1. Ativar ambiente virtual

```bash
cd backend
source .venv/bin/activate  # Linux/Mac
# OU
.venv\Scripts\activate     # Windows
```

### 2. Instalar dependências de teste

```bash
pip install pytest pytest-asyncio pytest-cov httpx python-dotenv
```

## Executando os Testes

### Rodar todos os testes unitários

```bash
pytest tests/unit/ -v
```

### Rodar testes com cobertura

```bash
pytest tests/unit/ --cov=app --cov-report=term-missing
```

### Rodar testes específicos

```bash
# Por arquivo
pytest tests/unit/test_schemas.py -v

# Por classe
pytest tests/unit/test_schemas.py::TestAuthSchemas -v

# Por função
pytest tests/unit/test_schemas.py::TestAuthSchemas::test_login_request_valid -v
```

### Rodar apenas testes que usam Supabase

```bash
pytest -m supabase -v
```

### Rodar apenas testes rápidos (smoke)

```bash
pytest -m smoke -v
```

### Rodar com output detalhado

```bash
pytest tests/unit/ -vv --tb=long
```

## Cobertura de Testes

### Testes Implementados

#### ✅ test_schemas.py (17 testes)
- Validação de LoginRequest e LoginResponse
- Validação de CheckRequest, CheckResponse e CheckStatusResponse
- Validação de HistoryItem
- Testes de campos obrigatórios e opcionais
- Validação de tipos de dados

#### ✅ test_models.py (13 testes)
- Estrutura da tabela CheckRecord
- Validação de colunas e tipos
- Constraints (primary key, nullable, defaults)
- Criação de instâncias do modelo

#### ✅ test_auth_router.py (14 testes)
- Endpoint de login
- Validação de credenciais
- Estrutura de resposta
- Tratamento de erros
- Métodos HTTP permitidos

#### ✅ test_check_router.py (24 testes) **[ATUALIZADO COM MOCKS]**
- Submissão de textos para análise
- Geração de IDs únicos (UUID)
- Consulta de status de análise
- **Mock do cliente Supabase**
- **Tratamento de erros de banco de dados**
- Validação de campos
- Fluxo completo (submit → query)

#### ✅ test_history_router.py (23 testes) **[ATUALIZADO COM MOCKS]**
- Consulta de histórico
- **Mock do cliente Supabase**
- **Tratamento de erros de banco de dados**
- Estrutura de itens
- Validação de campos e formatos
- Truncamento de preview de texto
- Ordenação por data (mais recente primeiro)
- Unicidade de IDs

### Total: **91 testes unitários** (atualizado)

## Mocking do Supabase

Os testes agora usam `unittest.mock` para simular o comportamento do Supabase:

```python
@pytest.fixture
def mock_supabase():
    """Mock do cliente Supabase para testes unitários"""
    with patch("app.routers.check.supabase") as mock:
        yield mock

def test_submit_check_success(mock_supabase):
    """Testa submissão bem-sucedida com Supabase mockado"""
    mock_response = MagicMock()
    mock_response.data = [{"id": "test-id"}]
    mock_response.error = None
    mock_supabase.table().insert().execute.return_value = mock_response
    
    response = client.post("/api/check/", json={"text": "Teste"})
    assert response.status_code == 200
```

### Testes de Erro Adicionados

- ✅ **Database unavailable (503)**: Quando Supabase retorna erro
- ✅ **Check not found (404)**: Quando registro não existe
- ✅ **Connection failures**: Tratamento de falhas de rede

## Próximos Passos

1. ✅ Testes Unitários - **CONCLUÍDO**
2. ⏳ Testes de Integração - **PRÓXIMA ETAPA**
   - Integração com banco de dados Supabase real
   - Testes de fluxo completo end-to-end
   - Testes de autenticação com JWT real
3. ⏳ Testes E2E (Opcional)
   - Fluxo completo da aplicação

## Observações Importantes

### Sobre o Supabase

- **Testes Unitários**: Usam mocks (sem conexão real)
- **Testes de Integração**: Usarão Supabase de teste/staging
- **Variáveis de Ambiente**: Configuradas automaticamente em `conftest.py`

### Variáveis de Ambiente para Testes

O `conftest.py` configura automaticamente:

```python
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SUPABASE_HTTP"] = "1"
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "test-key-12345"
```

Isso evita que testes unitários tentem conectar ao Supabase real.

### Isolamento de Testes

- Cada teste é **independente** e não afeta outros
- **Mocks** garantem que não há chamadas reais ao banco
- **Fixtures** fornecem dados consistentes para todos os testes

## Troubleshooting

### Erro de importação do Supabase

```bash
# Instale o cliente Supabase
pip install supabase
```

### Erro "SUPABASE_URL not set"

Os testes unitários NÃO precisam de Supabase real. Verifique se o `conftest.py` está presente:

```bash
ls backend/tests/conftest.py
```

### Testes falhando após mudanças

```bash
# Limpe cache do pytest
pytest --cache-clear

# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

### Mock não funciona

Certifique-se de que está usando a fixture correta:

```python
def test_example(mock_supabase):  # ← Adicione a fixture aqui
    # Seu teste aqui
    pass
```

## Comandos Úteis

```bash
# Rodar todos os testes
pytest tests/unit/ -v

# Rodar com cobertura detalhada
pytest tests/unit/ --cov=app --cov-report=html
open htmlcov/index.html  # Ver relatório no navegador

# Rodar testes de um módulo específico
pytest tests/unit/test_check_router.py -v

# Rodar testes com palavra-chave
pytest tests/unit/ -k "check" -v

# Mostrar prints durante testes
pytest tests/unit/ -v -s

# Parar no primeiro erro
pytest tests/unit/ -x
```

## Estrutura de um Teste com Mock

```python
def test_exemplo(mock_supabase):
    """Template de teste com Supabase mockado"""
    # 1. Configurar mock
    mock_response = MagicMock()
    mock_response.data = {"id": "123", "status": "OK"}
    mock_response.error = None
    mock_supabase.table().select().execute.return_value = mock_response
    
    # 2. Executar ação
    response = client.get("/api/endpoint")
    
    # 3. Verificar resultado
    assert response.status_code == 200
    assert response.json()["id"] == "123"
```

## Contribuindo

Ao adicionar novos testes:

1. ✅ Use mocks para dependências externas (Supabase, APIs)
2. ✅ Siga o padrão PEP-8
3. ✅ Adicione docstrings descritivas
4. ✅ Teste casos de sucesso E erro
5. ✅ Mantenha testes independentes
6. ✅ Use fixtures quando apropriado