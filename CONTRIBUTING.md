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

### Setup

➡️ **[Acesse o Guia de Build (BUILD.md)](./BUILD.md)**

---

## 🔄 Fluxo de Contribuição

### 1. Crie uma Branch

Para manter a segurança e organização do código, seguimos regras estritas:
* `main`: Contém apenas código de produção estável.
  * 🚫 Proibido: Fazer commit direto (push) na main.
  * ✅ Permitido: Apenas via Pull Request (PR) aprovado.

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

#### Para que seu código seja aceito, ele deve passar pelo seguinte checklist:

1. **Sync**: Garanta que sua branch está atualizada com a main (git pull origin main).
1. **Testes**: Rode os testes locais antes de enviar (pytest).
1. **Code** Review: O PR exige aprovação de pelo menos 1 membro da equipe.
1. **Descrição**: Preencha o template do PR explicando o que foi feito.

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