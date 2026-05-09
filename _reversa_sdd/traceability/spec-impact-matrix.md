# Spec Impact Matrix

> Gerado pelo Arquiteto em 2026-05-02

Matriz de impacto entre componentes — qual componente impacta quais outros.

---

## Componentes do Sistema

| ID | Componente | Tipo |
|----|------------|------|
| C01 | data_source.R — conexão PostgreSQL | Script |
| C02 | data_source.R — queries SQL | Query |
| C03 | tratamento_dados.R — transformação | Script |
| C04 | tratamento_dados.R — incluir_Situacao | Função |
| C05 | tratamento_dados.R — montarTabelaDisciplinas | Função |
| C06 | analise_ml.R — gerar_modelos | Função |
| C07 | analise_ml.R — realizar_previsao | Função |
| C08 | ETL Pentaho | Pipeline |
| C09 | Base Analítica PostgreSQL | Banco |

---

## Matriz de Impacto

| De \ Para | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 |
|-----------|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| **C01** (conexão) | — | | ● | | | | | | ● |
| **C02** (queries) | | — | ● | | | | | | ● |
| **C03** (transformação) | | | — | ● | ● | | | | |
| **C04** (incluir_Situacao) | | | | — | | ● | | | |
| **C05** (montarTabela) | | | | | — | ● | ● | | |
| **C06** (gerar_modelos) | | | | | | — | | ● | |
| **C07** (realizar_previsao) | | | | | | | — | | |
| **C08** (ETL) | | | | | | | | — | ● |
| **C09** (Base PostgreSQL) | ● | ● | | | | | | | — |

---

## Legenda

- ● = Dependência direta (componente A usa/comunica com componente B)

---

## Descrição dos Impactos

| De | Para | Descrição |
|----|------|------------|
| C01 (conexão) | C09 | Conecta ao PostgreSQL |
| C02 (queries) | C09 | Executa queries no PostgreSQL |
| C03 (trans) | C04 | Chama função incluir_Situacao |
| C03 (trans) | C05 | Chama função montarTabelaDisciplinas |
| C04 (situacao) | C06 | Fornece dados transformados para modelo |
| C05 (tabela) | C06 | Fornece pivô para treinamento |
| C05 (tabela) | C07 | Fornece pivô para previsão |
| C06 (modelos) | C08 | Salva modelos em arquivos |
| C09 (Base) | C01 | Fornece dados para conexão |
| C09 (Base) | C02 | Fornece dados para queries |

---

## Arquivos por Componente

| Componente | Arquivo | Linha |
|------------|---------|-------|
| C01 | data_source.R | 196-210 |
| C02 | data_source.R | 8-31 |
| C03 | tratamento_dados.R | 1-200 |
| C04 | tratamento_dados.R | 16-25 |
| C05 | tratamento_dados.R | 25-42 |
| C06 | analise_ml.R | 91-442 |
| C07 | analise_ml.R | 560-620 |
| C08 | pentaho/transforms/carregar-dados-analiticos.ktr | — |
| C09 | PostgreSQL (base_analitica) | — |

---

## Dívidas Técnicas Identificadas

| Origem | Impacto | Descrição |
|--------|---------|------------|
| C01 | Alto | Credenciais hardcoded |
| C03 | Médio | Funções duplicadas (le_dados/le_dados1) |
| C06 | Alto | Sem testes unitários |
| C09 | Médio | Sem backup automatizado |

---

## Escalas de Confiança

| Item | Confiança |
|------|-----------|
| Dependências entre scripts R | 🟢 CONFIRMADO |
| ETL → Base de dados | 🟢 CONFIRMADO |
| Funções → arquivos | 🟡 INFERIDO |

---

## Ver Também

- [c4-components.md](../c4-components.md) — Diagrama de componentes
- [architecture.md](../architecture.md) — Arquitetura geral