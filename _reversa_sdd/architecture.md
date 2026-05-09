# Arquitetura do Sistema — sigaa-sigra-retencao

> Gerado pelo Arquiteto em 2026-05-02

---

## 1. Visão Geral

Sistema de **predição de evasão acadêmica** utilizando machine learning. O sistema extrai dados do SIGAA/SIGRA, processa e treina modelos preditivos para identificar alunos em risco de evasão.

---

## 2. Componentes Principais

| Componente | Tipo | Responsabilidade | Tecnologia |
|-----------|------|------------------|------------|
| **ETL Pentaho** | Pipeline | Extração e carga de dados para warehouse | Pentaho DI |
| **Base Analítica** | Banco de Dados | Armazenamento de dados consolidados | PostgreSQL |
| **data_source.R** | Script R | Conexão e consultas ao banco | R + RPostgres |
| **tratamento_dados.R** | Script R | Transformação e preparação de dados | R + tidyverse |
| **analise_ml.R** | Script R | Treinamento e previsão de modelos | R + caret/h2o |

---

## 3. Fluxo de Dados

```
SIGAA ─────┐
           │       ETL         Base
SIGRA ─────┤──▶ Pentaho ───▶ Analítica
           │     (Kettle)    (PostgreSQL)

Base Analítica ──▶ data_source.R ──▶ tratamento_dados.R ──▶ analise_ml.R
                                              │                    │
                                              ▼                    ▼
                                    Tabela Modelo          Previsões
```

---

## 4. Integrações Externas

| Sistema | Tipo | Protocolo | Dados |
|---------|------|-----------|-------|
| **SIGAA** | Sistema acadêmico | JDBC → PostgreSQL | Alunos, disciplinas, notas |
| **SIGRA** | Sistema acadêmico | JDBC → PostgreSQL | Alunos, disciplinas, notas |
| **PostgreSQL** | Banco de dados | RPostgres | Base analítica |
| **Pentaho** | ETL | Kettle (.ktr) | Pipeline de dados |

---

## 5. Estrutura de Diretórios

```
sigaa-sigra-retencao/
├── data_source.R              # Conexão PostgreSQL
├── tratamento_dados.R         # Transformação de dados
├── analisar-evasao-sigaa-sigra.R  # Modelos ML
├── SQL/
│   ├── UNION_SIGAA_SIGRA.sql
│   ├── DADOS_SIGAA.sql
│   └── DADOS_SIGRA.sql
├── pentaho/
│   └── transforms/
│       └── carregar-dados-analiticos.ktr
└── arquivos/
    ├── modelos/              # Modelos treinados (.Rdata)
    ├── resultado/            # Métricas por coorte
    ├── previsoes/            # Alunos previstos
    └── logs/                 # Erros
```

---

## 6. Decisões Arquiteturais

| Decisão | Justificativa |
|---------|---------------|
| Linguagem R | Ecossistema maduro para ML e análise estatística |
| PostgreSQL | Banco existente da UnB com dados acadêmicos |
| Pentaho ETL | Ferramenta corporativa da UnB para ETL |
| F1-Score >= 0.7 | Threshold para aceitar modelos (ADR-001) |
| Exclusão Engenharia | Dados inconsistentes filtrados (ADR-002) |

---

## 7. Dívidas Técnicas

| Item | Severidade | Descrição |
|------|------------|------------|
| Credenciais hardcoded | 🔴 Alta | Banco com user/senha em código |
| Funções duplicadas | 🟡 Média | le_dados e le_dados1 são idênticas |
| Sem testes | 🔴 Alta | Nenhum teste automatizado |
| Sem config externa | 🟡 Média | Parâmetros hardcoded |

---

## 8. Escalas de Confiança

| Artefato | Confiança |
|----------|-----------|
| Componentes principais | 🟢 CONFIRMADO |
| Fluxo de dados | 🟢 CONFIRMADO |
| Integrações | 🟢 CONFIRMADO |
| Decisões arquiteturais | 🟡 INFERIDO |

---

## 9. Ver Também

- [c4-context.md](c4-context.md) — Diagrama C4 Contexto
- [c4-containers.md](c4-containers.md) — Diagrama C4 Containers
- [c4-components.md](c4-components.md) — Diagrama C4 Componentes
- [erd-complete.md](erd-complete.md) — ERD Completo
- [traceability/spec-impact-matrix.md](traceability/spec-impact-matrix.md) — Matriz de Impacto