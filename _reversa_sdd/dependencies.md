# Dependências do Projeto — sigaa-sigra-retencao

> Gerado pelo Scout em 2026-05-01

## Dependências R

### Instaladas no Script Principal

```r
install.packages("janitor")
install.packages("tidyverse")
install.packages("h2o")
install.packages("caTools")
install.packages("caret")
install.packages("rpart.plot")
install.packages('ranger')
```

### Bibliotecas Carregadas

```r
library(tidyverse)
library(C50)
library(caTools)
library(caret)
library(rpart)
library(rpart.plot)
library(h2o)
library(ranger)
library(RPostgres)
library(stringr)
```

---

## Dependências do Banco de Dados

| Componente | Detalhes |
|------------|----------|
| **DBMS** | PostgreSQL |
| **Driver** | RPostgres |
| **Host** | localhost |
| **Port** | 5432 |
| **Database** | postgres |
| **Schema** | base_analitica |

---

## Schema do Banco de Dados

### Tabela: `base_analitica.alunos_sigaa_sigra_27092022`

Colunas principais:
- `matricula` / `id_pessoa` — Identificador do aluno
- `sexo` — Gênero
- `status_discente` — Status do aluno (ATIVO, CONCLUÍDO, TRANCADO, etc.)
- `ano_ingresso` / `periodo_ingresso` — Coorte de ingresso
- `nome_curso` — Nome do curso
- `opção` — Código da opção/turno
- `sigla_campus` / `nome_campus` — Campus
- `codigo_comp_curricular` / `id_disciplina` — Código da disciplina
- `nome_comp_curricular` — Nome da disciplina
- `tipo_integralizacao` — Tipo (OB, OBR, OPT)
- `conceito` — Nota/Conceito
- `numero_faltas_mc` — Número de faltas
- `fonte` — SIGAA ou SIGRA

---

## Dependências Externas

| Sistema | Versão | Papel |
|---------|--------|-------|
| SIGAA (UnB) | — | Sistema acadêmico fonte |
| SIGRA (UnB) | — | Registro acadêmico fonte |
| Pentaho | — | ETL para warehouse |
| R | 4.x | Runtime |
| RStudio | — | IDE |

---

## Credenciais (Hardcoded)

As credenciais estão hardcoded em `data_source.R`:
- Usuário: `postgres`
- Senha: `123456`
- Host: `localhost:5432`