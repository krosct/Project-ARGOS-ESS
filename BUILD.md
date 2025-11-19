# Build & Setup

# 🐳 Opção 1: Rodando com Docker (Recomendado)

Esta é a maneira mais rápida de rodar a aplicação completa (Frontend + Backend + Banco de Dados) sem configurar ambientes locais.

## 1. Pré-requisitos

* Docker
* Docker Compose

## 2. Execução

1. Na raiz do projeto, execute:

```bash
docker-compose up --build
```

2. Acesse os serviços:

* **Frontend**: http://localhost:3000
* **API Backend**: http://localhost:8000/docs

# 🐍 Opção 2: Instalação Manual (Desenvolvimento Local)
Use esta opção se precisar debugar código ou se não quiser usar Docker.

## 1. Pré-requisitos

* **Python 3.11+** (ou versão compatível)
* **pip** (gerenciador de pacotes do Python)
* **Git**
* **Virtualenv**

> **Observação:** Para usuários Windows, recomenda-se instalar o [Python via Microsoft Store](https://www.microsoft.com/store/productId/9P7QFQMJRFP7) ou [python.org](https://www.python.org/downloads/).

---

## 2. Clonar o Repositório

```bash
git clone https://github.com/krosct/Projeto-ESS.git
cd Projeto-ESS/
```

---

## 3. Criar Ambiente Virtual (opcional, mas recomendado)

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## 4. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Configuração Inicial

1. Crie um arquivo `.env` na raiz do projeto:

   ```bash
   touch .env
   ```
2. Adicione as variáveis de configuração:

   ```
   API_KEY=your_api_key_here
   MODEL_PATH=path_to_trained_model
   DATABASE_URL=postgresql://user:pass@localhost:5432/argos
   ```

---

## 6. Executar o Sistema

### 6.1 Executar via terminal

```bash
python main.py
```
