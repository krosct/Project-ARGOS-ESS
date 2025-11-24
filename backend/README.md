# Requisitos

- Python 3.9+
- PostgreSQL (Instalado e rodando)

# Instalação

1. Crie um ambiente virtual:

```bash
python -m venv venv
```
   
2. Ative o ambiente:

```bash
source venv/bin/activate
```

3. Instale as dependências:
   
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:

Crie o .env com a conexão com o banco de dados.

# Execução

Rode o servidor de desenvolvimento:

`uvicorn app.main:app --reload`
