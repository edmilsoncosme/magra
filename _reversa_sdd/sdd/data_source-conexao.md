# data_source — Conexão PostgreSQL

## Visão Geral

Módulo de conexão com o banco de dados PostgreSQL para extração de dados acadêmicos do SIGAA e SIGRA. Fornece funções para estabelecer conexões, executar queries e retornar DataFrames.

## Responsabilidades

- Estabelecer conexão com PostgreSQL (localhost:5432)
- Executar queries SQL parametrizadas
- Retornar resultados como DataFrames do R
- Gerenciar desconexão automática após consultas

## Interface

```r
conectar() -> DBIConnection
desconectar(conexao) -> void
le_dados(conexao, strQuery) -> data.frame
le_dados1(conexao, sql) -> data.frame
le_dados2(conexao, strQuery, strWhere) -> data.frame
```

### Parâmetros

| Função | Parâmetro | Tipo | Obrigatório | Descrição |
|--------|-----------|------|--------------|------------|
| conectar | — | — | — | Sem parâmetros |
| desconectar | conexao | DBIConnection | Sim | Conexão ativa |
| le_dados | conexao | DBIConnection | Sim | Conexão ativa |
| le_dados | strQuery | character | Sim | Query SQL |
| le_dados1 | conexao | DBIConnection | Sim | Conexão ativa |
| le_dados1 | sql | character | Sim | Query SQL |
| le_dados2 | conexao | DBIConnection | Sim | Conexão ativa |
| le_dados2 | strQuery | character | Sim | Query base |
| le_dados2 | strWhere | character | Sim | Cláusula WHERE |

### Retorno

| Função | Tipo | Descrição |
|--------|------|------------|
| conectar | DBIConnection | Objeto de conexão |
| desconectar | void | NULL invisível |
| le_dados | data.frame | Dados da query |
| le_dados1 | data.frame | Dados da query |
| le_dados2 | data.frame | Dados da query com filtro |

## Regras de Negócio

- Conexão usa host `localhost`, porta `5432`, banco `postgres` 🟢
- Usuário `postgres`, senha `123456` (hardcoded) 🟡
- `le_dados` executa query e desconecta automaticamente (não retorna conexão) 🟡
- `le_dados1` é idêntico a `le_dados` — código duplicado 🟡
- `le_dados2` usa variável `con` hardcoded em vez do parâmetro `conexao` 🟡

## Fluxo Principal

1. **Conectar**: `conectar()` → DBIConnection
2. **Executar Query**: `le_dados(conexao, query)` → data.frame
3. **Desconectar**: Automático via `dbDisconnect()`

### Fluxo le_dados()

```r
1. Recebe conexao e strQuery
2. Executa dbGetQuery(conexao, strQuery)
3. Desconecta com dbDisconnect(conexao)
4. Retorna data.frame
```

### Fluxo le_dados2()

```r
1. Recebe conexao, strQuery, strWhere
2. Monta query completa: strQuery + " WHERE " + strWhere
3. Usa dbBind para parâmetros
4. Executa e retorna data.frame
```

## Fluxos Alternativos

- **Query vazia**: Retorna data.frame vazio (0 linhas) sem erro
- **Conexão inválida**: Erro em dbGetQuery (não tratado)
- **Timeout**: Não há timeout configurado 🟡

## Dependências

- **RPostgres** — Driver PostgreSQL para R 🟢
- **DBI** — Interface de banco de dados 🟢

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Performance | Queries simples executam em < 5s | Sem evidência | 🔴 |
| Segurança | Credenciais expostas em código | `data_source.R:196-200` | 🟢 |
| Disponibilidade | Sem retry em falha de conexão | Sem evidência | 🔴 |

> ⚠️ Credenciais hardcoded são dívida técnica crítica.

## Critérios de Aceitação

```gherkin
Dado que o banco PostgreSQL está acessível em localhost:5432
Quando executar conectar()
Então deve retornar um objeto DBIConnection válido

Dado que uma conexão ativa existe e uma query válida foi fornecida
Quando executar le_dados(conexao, "SELECT * FROM tabela")
Então deve retornar um data.frame com os resultados

Dado que a conexão está ativa mas o banco está indisponível
Quando executar le_dados(conexao, query)
Então deve lançar um erro de conexão
```

## Prioridade

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Conexão PostgreSQL | Must | Caminho crítico — todas as queries dependem |
| Execução de queries | Must | Função principal do módulo |
| Gerenciamento de desconexão | Should | Previne vazamento de conexões |
| Query parametrizada (le_dados2) | Could | Função com bug (usa `con` hardcoded) |
| Duplicate code (le_dados1) | Won't | Tech debt não prioritário |

## Rastreabilidade de Código

| Arquivo | Função | Cobertura |
|---------|--------|-----------|
| `data_source.R` | conectar() | 🟢 |
| `data_source.R` | desconectar() | 🟢 |
| `data_source.R` | le_dados() | 🟢 |
| `data_source.R` | le_dados1() | 🟢 |
| `data_source.R` | le_dados2() | 🟡 — usa `con` hardcoded |

---

**Próximo:** data_source-queries.md — Queries SQL. Digite **CONTINUAR** para prosseguir.