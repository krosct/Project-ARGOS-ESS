# Como Contribuir com o Project Argos

Obrrigado por seu interesse em contribuir com o **Project Argos**! Este guia estabelece as práticas e padrões para mantermos nosso projeto organizado, colaborativo e de alta qualidade.

---

## 📖 Sobre o Projeto

O **Project Argos** é uma plataforma de IA para detecção de fake news. Estamos no início do desenvolvimento, aplicando boas práticas de Engenharia de Software para construir uma solução robusta contra a desinformação.

---

## 🤝 Código de Conduta

- **Respeito mútuo:** Feedbacks construtivos focados no código
- **Colaboração:** Ajude e compartilhe conhecimento
- **Foco:** Aprender e construir um ótimo produto

---

## 🛠️ Configurando o Ambiente

### Pré-requisitos
- Python 3.11+
- Git configurado em sua máquina

### Setup

```bash
# Clone o repositório
git clone https://github.com/krosct/Project-ARGOS-ESS.git
cd Project-ARGOS-ESS

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## 🔄 Fluxo de Contribuição

### 1. Crie uma Branch

Nunca trabalhe direto na `main`. Use prefixos:

- `feature/` - Nova funcionalidade
- `fix/` - Correção de bug
- `docs/` - Documentação
- `refactor/` - Refatoração
- `model/` - Alterações em modelos de IA

```bash
git checkout main
git pull origin main
git checkout -b feature/nome-descritivo
```

### 2. Faça Commits

Use mensagens claras com prefixos:

```bash
git commit -m "feat: adiciona validação de URLs"
git commit -m "fix: corrige erro no classificador"
git commit -m "docs: atualiza README"
```

### 3️. Abra um Pull Request (PR)

Quando seu trabalho estiver completo e testado:

```bash
# Envie sua branch para o repositório remoto
git push origin feature/nome-da-sua-branch
```

#### Criando um Pull Request

Ao abrir um PR, inclua:

- **Título claro**: Seja objetivo (ex: "Adiciona análise de sentimento para detecção de fake news")
- **Descrição detalhada**: 
  - Resuma as mudanças realizadas
  - Explique o problema resolvido
  - Mencione issues relacionadas usando `Resolve #<número>`
  - Adicione screenshots ou logs se relevante
- **Como testar**: Liste os passos para validar suas alterações

Aguarde a revisão de pelo menos um membro da equipe. Esteja aberto a feedbacks e ajustes!

---

## 📝 Boas Práticas

### Código
- Siga a **PEP 8**, o guia de estilo oficial do Python
- Use nomes descritivos para variáveis, funções e classes
- Mantenha funções pequenas e com responsabilidade única
- Adicione docstrings em funções e classes
- Comente lógicas complexas, especialmente em modelos de IA

### 🔒 Segurança

🚨 **NUNCA** faça commit de chaves de API, tokens ou senhas!

Use variáveis de ambiente com `.env`.

### 📦 Gerenciamento de Dependências

Ao adicionar uma nova biblioteca:

```bash
# Instale a biblioteca
pip install nome-da-biblioteca

# Atualize o requirements.txt
pip freeze > requirements.txt
```

### ✅ Testes

Antes de abrir um PR:

- Execute todos os testes existentes
- Adicione testes para novas funcionalidades
- Teste integrações com APIs externas
- Valide a performance do modelo se aplicável

```bash
# Execute os testes
pytest

# Execute com cobertura
pytest --cov
```

---

### Reportando Bugs

Ao reportar um bug, inclua:

1. Descrição clara do problema
2. Passos para reproduzir
3. Comportamento esperado vs. comportamento atual
4. Ambiente (SO, versão do Python, dependências)
5. Logs ou mensagens de erro relevantes

---

## 🙏 Agradecimentos

Obrigado por contribuir com o **Project Argos** e ajudar a combater a desinformação! Cada contribuição, por menor que seja, nos ajuda a construir uma internet mais confiável e segura.