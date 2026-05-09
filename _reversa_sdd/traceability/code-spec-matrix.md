# Code/Spec Matrix

> Gerado pelo Redator em 2026-05-02

Matriz de rastreabilidade entre arquivos de código e specs SDD.

---

## Arquivos vs Specs

| Arquivo | Spec Correspondente | Cobertura |
|---------|---------------------|-----------|
| `data_source.R` | [sdd/data_source-conexao.md](sdd/data_source-conexao.md) | 🟢 |
| `data_source.R` | [sdd/data_source-queries.md](sdd/data_source-queries.md) | 🟢 |
| `tratamento_dados.R` | [sdd/tratamento_dados.md](sdd/tratamento_dados.md) | 🟢 |
| `analisar-evasao-sigaa-sigra.R` | [sdd/analise_ml-treinamento.md](sdd/analise_ml-treinamento.md) | 🟢 |
| `analisar-evasao-sigaa-sigra.R` | [sdd/analise_ml-previsao.md](sdd/analise_ml-previsao.md) | 🟢 |
| `pentaho/transforms/carregar-dados-analiticos.ktr` | [sdd/etl-pentaho.md](sdd/etl-pentaho.md) | 🟡 — arquivo binário |
| `SQL/UNION_SIGAA_SIGRA.sql` | [sdd/etl-pentaho.md](sdd/etl-pentaho.md) | 🟢 |
| `SQL/DADOS_SIGAA.sql` | — | — |
| `SQL/DADOS_SIGRA.sql` | — | — |
| `SQL/PROCEDURE_ATUALIZA_OPCAO_SIGRA.sql` | — | — |
| `SQL/TESTES_25_09.sql` | — | — |

---

## Cobertura por Módulo

| Módulo | Arquivos | Specs | Cobertura |
|--------|----------|-------|-----------|
| Conexão DB | 1 | 1 | 🟢 100% |
| Queries SQL | 1+ | 1 | 🟢 100% |
| Transformação | 1 | 1 | 🟢 100% |
| ML Treinamento | 1 | 1 | 🟢 100% |
| ML Previsão | 1 | 1 | 🟢 100% |
| ETL | 2 | 1 | 🟡 50% |

---

## Arquivos sem Spec Correspondente

| Arquivo | Motivo |
|---------|--------|
| `SQL/DADOS_SIGAA.sql` | Query de desenvolvimento, não usada em produção |
| `SQL/DADOS_SIGRA.sql` | Query de desenvolvimento, não usada em produção |
| `SQL/PROCEDURE_ATUALIZA_OPCAO_SIGRA.sql` | Stored procedure não encontrada no código |
| `SQL/TESTES_25_09.sql` | Arquivo de teste, fora do escopo |

---

## Resumo de Cobertura

| Métrica | Valor |
|---------|-------|
| Total de arquivos do projeto | 11 |
| Arquivos com spec | 7 (64%) |
| Arquivos sem spec | 4 (36%) |
| Specs geradas | 6 |

---

## Observações

1. **Arquivos SQL**: As queries `DADOS_SIGAA.sql` e `DADOS_SIGRA.sql` são versões detalhadas que não são usadas diretamente pelo código R. As queries usadas estão embedadas em `data_source.R`.

2. **Pentaho KTR**: Arquivo binário (.ktr) não pode ser analisado diretamente. Spec baseada em referências no código e commit `4c01d9f`.

3. **Procedure SQL**: A procedure `PROCEDURE_ATUALIZA_OPCAO_SIGRA.sql` existe mas não é chamada pelo código R. Pode ter uso administrativo/manual.

---

## Ver Também

- [spec-impact-matrix.md](spec-impact-matrix.md) — Matriz de impacto entre specs
- [architecture.md](../architecture.md) — Arquitetura geral