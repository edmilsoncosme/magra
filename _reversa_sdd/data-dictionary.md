# Dicionário de Dados — sigaa-sigra-retencao

> Gerado pelo Archaeologist em 2026-05-01

---

## Tabela: base_analitica.alunos_sigaa_sigra_27092022

**Descrição:** View/tabela unificada de alunos do SIGAA e SIGRA

| Campo | Tipo | Obrigatório | Descrição | Valores |
|-------|------|--------------|------------|---------|
| matricula | text | Sim | Identificador do aluno | - |
| id_pessoa | integer | Sim | ID interno da pessoa | - |
| sexo | text | Não | Gênero | M/F |
| status_discente | text | Sim | Status atual do aluno | ATIVO, CONCLUÍDO, CANCELADO, TRANCADO, FORMANDO, DESLIGADO, Formatura, etc. |
| ano_ingresso | integer | Sim | Ano de entrada | 2010-2022 |
| periodo_ingresso | integer | Sim | Período de entrada | 1/2 |
| ano_saiu | integer | Não | Ano de saída/conclusão | - |
| nome_curso | text | Sim | Nome do curso | CIÊNCIA POLÍTICA, ENGENHARIA, etc. |
| periodo_curso | integer | Não | Período atual do curso | - |
| opcao | text | Não | Código da opção/turno | - |
| sigla_campus | text | Sim | Sigla do campus | FGA, etc. |
| nome_campus | text | Sim | Nome do campus | - |
| codigo_comp_curricular | text | Sim | Código da disciplina | - |
| id_disciplina | integer | Não | ID da disciplina | - |
| nome_comp_curricular | text | Sim | Nome da disciplina | - |
| descricao_tipo_disciplina | text | Sim | Tipo do componente | DISCIPLINA |
| cod_dis_sigra | integer | Não | Código equivalente no SIGRA | - |
| equivalencia_disciplina | text | Não | Equivalência | - |
| sigla_dep | text | Não | Sigla do departamento | - |
| nome_dep | text | Não | Nome do departamento | - |
| tipo_integralizacao | text | Sim | Tipo de integralização | OB, OBR, OPT |
| tipo_integralizacao_des | text | Não | Descrição do tipo | - |
| conceito | text | Sim | Nota/conceito | A, B, C, D, E, O, etc. |
| numero_faltas_mc | integer | Não | Número de faltas | - |
| fonte | text | Sim | Sistema de origem | sigaa / sigra |

---

## Tabela: Base de Treinamento (Modelo)

**Descrição:** Tabela pivot gerada para treino dos modelos ML

| Campo | Tipo | Descrição |
|-------|------|------------|
| Linha: matricula | text | Identificador do aluno |
| Colunas: códigos de disciplinas | integer | Quantidade de vezes que cursou |
| Coluna: situacao | factor | Target: FORMADO / EVADIDO |

---

## Query: sigaa (Treinamento FGA)

**Filtros aplicados:**
- `fonte = 'sigaa'`
- `sigla_campus = 'FGA'`
- `descricao_tipo_disciplina = 'DISCIPLINA'`
- `conceito IS NOT NULL`
- `status_discente IN ('CONCLUÍDO', 'CANCELADO', 'ATIVO - FORMANDO', 'DESLIGADO', 'FORMADO', 'Formatura', 'TRANCADO')`
- `nome_curso NOT IN ('ENGENHARIA')`

---

## Query: sigra (Treinamento FGA)

**Filtros aplicados:**
- `fonte = 'sigra'`
- `sigla_campus = 'FGA'`
- `descricao_tipo_disciplina = 'DISCIPLINA'`
- `conceito IS NOT NULL`
- `status_discente IN ('Transferência', 'TRANCADO', 'Formatura', 'FORMADO', 'DESLIGADO', 'CONCLUÍDO', 'CANCELADO', 'ATIVO - FORMANDO')`
- `nome_curso NOT IN ('Engenharia')`
- `opcao IS NOT NULL`

---

## Query: sigaa_ativos (Previsão FGA)

**Filtros aplicados:**
- `fonte = 'sigaa'`
- `sigla_campus = 'FGA'`
- `status_discente = 'ATIVO'`

---

## Definição: Situação do Aluno

**Transformação:** `incluir_Situacao()`

| status_discente | situacao |
|-----------------|-----------|
| ATIVO - FORMANDO | FORMADO |
| CONCLUÍDO | FORMADO |
| Formatura | FORMADO |
| FORMADO | FORMADO |
| TRANCADO | EVADIDO |
| CANCELADO | EVADIDO |
| DESLIGADO | EVADIDO |
| Transferência | EVADIDO |

🟢 **CONFIRMADO** — direto do código em `tratamento_dados.R:16-18`

---

## Parâmetros de Treinamento

| Modelo | Parâmetro | Valor |
|--------|-----------|-------|
| C5.0 | trials | 10 |
| Random Forest | num.trees | 10 |
| Rede Neural | hidden | c(100) |
| Rede Neural | epochs | 1000 |
| Threshold | F1 mínimo | >= 0.7 |