# Issue Templates — Documentação Interna

Este arquivo documenta os templates de Issue usados pelo Projeto Argos e orienta manutenção e testes. Ele não é um template em si, mas uma referência para os arquivos YAML localizados em `.github/` (por exemplo: `bug_report.yml`, `feature_request.yml`, `config.yml`).

---

## Sumário

- [Issue Templates — Documentação Interna](#issue-templates--documentação-interna)
  - [Sumário](#sumário)
  - [Visão Geral](#visão-geral)
  - [Templates Principais](#templates-principais)
    - [`bug_report.yml` (Bug Report Form)](#bug_reportyml-bug-report-form)

---

## Visão Geral

Os templates padronizam informações mínimas necessárias para reportar bugs e sugerir features, garantindo que issues contenham contexto suficiente para triagem e implementação.

Arquivos relevantes:
- ` .github/bug_report.yml` — formulário para reportar bugs.
- ` .github/feature_request.yml` — formulário para novas funcionalidades.
- ` .github/config.yml` — configura o menu de criação de issues no repositório.

---

## Templates Principais

### `bug_report.yml` (Bug Report Form)
Propósito: coletar informações estruturadas ao reportar bugs.

Campos recomendados:
- Título conciso (automático)
- Descrição (passos para reproduzir) — obrigatório
- Resultado esperado vs. resultado atual — obrigatório
- Logs e screenshots — opcional (upload)
- Ambiente (SO, browser, versões) — obrigatório
- Prioridade / Componente — dropdown

Labels automáticas sugeridas: `bug`, `needs-triage`

Exemplo (resumo de configuração YAML form — apenas referência):
```yaml
name: Bug report
body:
  - type: textarea
    id: steps
    attributes:
      label: "Passos para reproduzir"
      description: "Descreva passo a passo"
      required: true
  - type: textarea
    id: expected
    attributes:
      label: "Comportamento esperado"
  - type: textarea
    id: actual
    attributes:
      label: "Comportamento atual"
  - type: dropdown
    id: component
    attributes:
      label: "Componente"
      options:
        - Frontend
        - Backend
        - IA