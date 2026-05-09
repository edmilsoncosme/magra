# data_source — Queries SQL

## Visão Geral

Conjunto de 10 queries SQL predefinidas para extração de dados acadêmicos do SIGAA e SIGRA. Cada query serve a um propósito específico (treinamento ou previsão) e filtra por campus e tipo de dado.

## Responsabilidades

- Definir queries SQL para extração de dados de treinamento
- Definir queries SQL para extração de dados de previsão
- Filtrar por campus (FGA, UnB) e sistema de origem (SIGAA, SIGRA)
- Excluir cursos inválidos ("Engenharia" genérico)

## Interface

```r
sigaa       # Query: Treinamento FGA (SIGAA)
sigra       # Query: Treinamento FGA (SIGRA)
sigaa_ativos # Query: Previsão FGA (SIGAA)
sigaa_sigra_todos # Query: Previsão FGA (SIGAA+SIGRA)
sigaa_sigra_cp # Query: Treinamento Ciência Política
sigaa_sigra_cp_todos # Query: Previsão Ciência Política
sigaa_cp_ativos # Query: Previsão Ciência Política
sigaa_sigra_unb # Query: Treinamento UnB (outros campuses)
sigaa_sigra_unb_todos # Query: Previsão UnB
sigaa_unb_ativos # Query: Previsão UnB
```

### Parâmetros de Todas as Queries

| Parâmetro | Valor | Descrição |
|-----------|-------|------------|
| Fonte | sigaa / sigra | Sistema de origem |
| Campus | FGA ou != FGA | Filtrar por campus |
| Tipo | DISCIPLINA | Apenas componentes do tipo disciplina |
| Conceito | IS NOT NULL | Apenas com nota registrada |
| Curso | NOT IN ('ENGENHARIA', 'Engenharia') | Excluir curso genérico |

### Tabela de Queries

| Query | Finalidade | Campus | Fonte |
|-------|------------|--------|-------|
| `sigaa` | Treinamento | FGA | SIGAA |
| `sigra` | Treinamento | FGA | SIGRA |
| `sigaa_ativos` | Previsão | FGA | SIGAA |
| `sigaa_sigra_todos` | Previsão | FGA | SIGAA+SIGRA |
| `sigaa_sigra_cp` | Treinamento | - | Ciência Política |
| `sigaa_sigra_cp_todos` | Previsão | - | Ciência Política |
| `sigaa_cp_ativos` | Previsão | - | Ciência Política |
| `sigaa_sigra_unb` | Treinamento | != FGA | UnB |
| `sigaa_sigra_unb_todos` | Previsão | != FGA | UnB |
| `sigaa_unb_ativos` | Previsão | != FGA | SIGAA |

## Regras de Negócio

- Todas as queries leem da view `base_analitica.alunos_sigaa_sigra_27092022` 🟢
- Queries de treinamento filtram por status em lista específica 🟢
- Queries de previsão filtram apenas `status_discente = 'ATIVO'` 🟢
- Curso "Engenharia" (genérico) excluído de todas as queries 🟢
- Campo `descricao_tipo_disciplina = 'DISCIPLINA'` 🟢
- Campo `conceito IS NOT NULL` 🟡

## Fluxo Principal

1. Carregar script `data_source.R` — queries ficam disponíveis como objetos globais
2. Chamar `le_dados(conexao, sigaa)` — executa query de treinamento FGA
3. Receber data.frame com resultados

### Exemplo de Query (sigaa)

```sql
SELECT *
FROM base_analitica.alunos_sigaa_sigra_27092022
WHERE fonte = 'sigaa'
  AND sigla_campus = 'FGA'
  AND descricao_tipo_disciplina = 'DISCIPLINA'
  AND conceito IS NOT NULL
  AND status_discente IN ('CONCLUÍDO', 'CANCELADO', 'ATIVO - FORMANDO', 'DESLIGADO', 'FORMADO', 'Formatura', 'TRANCADO')
  AND nome_curso NOT IN ('ENGENHARIA')
```

## Fluxos Alternativos

- **Query sem resultados**: Retorna data.frame vazio (0 linhas)
- **Coluna inexistente**: Erro do PostgreSQL não tratado
- **Conexão perdida durante execução**: Erro não tratado

## Dependências

- **Base Analítica PostgreSQL** — tabela `base_analitica.alunos_sigaa_sigra_27092022` 🟢
- **data_source-conexao.md** — usa função `le_dados()` 🟢

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Performance | Queries executam em < 30s | Sem evidência | 🔴 |
| Segurança | Sem dados sensíveis nas queries | Queries são de leitura | 🟢 |

## Critérios de Aceitação

```gherkin
Dado que a conexão com PostgreSQL está ativa
Quando executar le_dados(conexao, sigaa)
Então deve retornar data.frame com colunas: matricula, nome_curso, codigo_comp_curricular, conceito, status_discente

Dado que a conexão com PostgreSQL está ativa
Quando executar le_dados(conexao, sigaa_ativos)
Então deve retornar apenas alunos com status_discente = 'ATIVO'

Dado que a conexão com PostgreSQL está ativa mas a view não existe
Quando executar qualquer query
Então deve retornar erro de tabela inexistente
```

## Prioridade

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Queries de treinamento | Must | Essenciais para gerar modelos ML |
| Queries de previsão | Must | Essenciais para identificar alunos em risco |
| Filtro por campus | Should | Permite análise por unidade acadêmica |
| Filtro por curso | Should | Exclui dados inválidos |

## Rastreabilidade de Código

| Arquivo | Função | Cobertura |
|---------|--------|-----------|
| `data_source.R:8-31` | Definição das 10 queries | 🟢 |

---

**Próximo:** tratamento_dados.md — Transformação de dados. Digite **CONTINUAR** para prosseguir.