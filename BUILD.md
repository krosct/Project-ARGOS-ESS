# Build & Setup

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
   ```

---

## 6. Executar o Sistema

### 6.1 Executar via terminal

```bash
python main.py
```

---

## 7. Testes (opcional)

Se houver testes automatizados, rode:

```bash
pytest tests/
```

---

Quer que eu faça isso?
