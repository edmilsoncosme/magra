# Plano de Reconstrução — sigaa-sigra-retencao (Python)

> Baseado na Engenharia Reversa do Reversa (`_reversa_sdd/`)
> Este plano mapeia o sistema legado R para uma estrutura Python moderna, preservando as regras de negócio e funcionalidades existentes.

---

## 1. Estrutura de Diretórios Proposta

```
sigaa-sigra-python/
├── config/
│   └── .env                 # Credenciais (NOVO)
├── src/
│   ├── data_source/
│   │   ├── connection.py    # Conexão PostgreSQL
│   │   └── queries.py       # Queries SQL
│   ├── transform/
│   │   ├── situacao.py     # incluir_Situacao()
│   │   └── pivot.py        # montarTabelaDisciplinas()
│   ├── ml/
│   │   ├── train.py        # gerar_modelos()
│   │   └── predict.py      # realizar_previsao()
│   ├── etl/                # Pipeline ETL (alternativa ao Pentaho)
│   └── cli/                # Interface de linha de comando
│       ├── __init__.py
│       ├── main.py         # Entry point (Click)
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── train.py    # python -m cli train
│       │   ├── predict.py  # python -m cli predict
│       │   └── pipeline.py # python -m cli pipeline (completo)
│       └── options.py      # Argumentos compartilhados
├── tests/                  # Testes automatizados
├── docs/                   # Documentação
├── models/                 # Modelos treinados (.joblib)
├── output/
│   ├── resultados/         # Métricas por coorte
│   ├── previsoes/          # Alunos previstos
│   └── logs/               # Logs de execução
└── sql/
    └── referencias/        # Cópia das queries originais
```

---

## 2. Mapeamento Specs SDD → Módulos Python

### 2.1 data_source-conexao.md → Conexão PostgreSQL

| Original (R) | Python |
|--------------|--------|
| `conectar()` | `DatabaseConnection.connect()` |
| `desconectar()` | `DatabaseConnection.disconnect()` |
| `le_dados()` | `execute_query()` |
| `le_dados2()` | `execute_query_with_params()` |

**Dependências:** `psycopg2-binary`, `sqlalchemy`, `pandas`

**Melhoria:** Credenciais em `.env` (não mais hardcoded)

---

### 2.2 data_source-queries.md → Queries SQL

| Query | Finalidade | Campus |
|-------|------------|--------|
| `sigaa` | Treinamento | FGA |
| `sigra` | Treinamento | FGA |
| `sigaa_ativos` | Previsão | FGA |
| `sigaa_sigra_todos` | Previsão | FGA |
| `sigaa_sigra_cp` | Treinamento | Ciência Política |
| `sigaa_sigra_cp_todos` | Previsão | Ciência Política |
| `sigaa_cp_ativos` | Previsão | Ciência Política |
| `sigaa_sigra_unb` | Treinamento | UnB |
| `sigaa_sigra_unb_todos` | Previsão | UnB |
| `sigaa_unb_ativos` | Previsão | UnB |

**Filtros obrigatórios:**
- `nome_curso NOT IN ('ENGENHARIA', 'Engenharia')`
- `descricao_tipo_disciplina = 'DISCIPLINA'`
- `conceito IS NOT NULL`

---

### 2.3 tratamento_dados.md → Transformação de Dados

| Função R | Python |
|----------|--------|
| `incluir_Situacao()` | `incluir_situacao(df) -> df` |
| `montarTabelaDisciplinas()` | `TabelaPivot.montar()` |
| `inserirDisplinasCursadas()` | `TabelaPivot.inserir_contagens()` |
| `inserirSituacaoAluno()` | `TabelaPivot.inserir_situacao()` |
| `selecionarAlunos()` | `selecionar_alunos(df, filtros)` |

**RN-001 (Classificação de Situação):**
```python
FORMADO = {'ATIVO - FORMANDO', 'CONCLUÍDO', 'Formatura', 'FORMADO'}
EVADIDO = {'TRANCADO', 'CANCELADO', 'DESLIGADO', 'Transferência'}
```

---

### 2.4 analise_ml-treinamento.md → Treinamento de Modelos

| Modelo R | Biblioteca | Python |
|----------|------------|--------|
| C5.0 | C50 | `sklearn.tree.DecisionTreeClassifier` |
| Random Forest | ranger | `sklearn.ensemble.RandomForestClassifier` |
| RPart | rpart | `sklearn.tree.DecisionTreeClassifier` |
| Regressão Logística | glm | `sklearn.linear_model.LogisticRegression` |
| Rede Neural | h2o | `sklearn.neural_network.MLPClassifier` |

**RN-003 (Critério de Aceitação):**
> F1-Score >= 0.7 para aceitar modelo

**Loop de Treinamento:**
```
para cada curso:
  para cada opção (turno):
    para cada coorte (ano + período):
      se (existe FORMADO E EVADIDO):
        treinar 5 modelos
        se (F1 >= 0.7):
          salvar modelo .joblib
```

---

### 2.5 analise_ml-previsao.md → Previsão de Evasão

| Função | Descrição |
|--------|------------|
| `carregar_modelos()` | Carrega arquivos `.joblib` do disco |
| `filtrar_alunos_ativos()` | Filtra status = 'ATIVO' [RN-009] |
| `executar_previsao()` | Aplica modelo aos dados |
| `salvar_previsoes()` | Gera CSV com resultados |

**Saída:** `output/previsoes/previsao_evasao_[curso]_[opcao].csv`

---

### 2.6 etl-pentaho.md → ETL

**Status atual:** Execução manual no início do semestre

**Alternativa Python:** Apache Airflow ou script simples

---

### 2.7 CLI → Interface de Linha de Comando

A CLI é a camada de interface que permite ao operador executar o sistema via terminal.

#### Estrutura de Arquivos

```
src/cli/
├── __init__.py           # Package marker
├── main.py               # Entry point com Click
├── commands/
│   ├── __init__.py       # Package marker
│   ├── train.py          # Comando: treinar modelos
│   ├── predict.py        # Comando: executar previsões
│   └── pipeline.py       # Comando: pipeline completo
└── options.py            # Opções e argumentos compartilhados
```

#### Dependências

```python
click>=8.1.0      # Framework CLI
rich>=13.0.0      # Output formatado (opcional)
```

#### Comandos Disponíveis

##### Comando: `train`

```bash
python -m cli train --curso "CIENCIA POLITICA" --opcao "M" --f1-threshold 0.7
```

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|------------|
| `--curso` | str | Sim | - | Nome do curso |
| `--opcao` | str | Não | Todas | Turno (M/T/N) |
| `--tipo` | str | Não | OB | Tipo: OB, OBR, OPT |
| `--f1-threshold` | float | Não | 0.7 | Threshold F1-Score |
| `--output` | str | Não | ./models/ | Pasta de saída |

##### Comando: `predict`

```bash
python -m cli predict --curso "CIENCIA POLITICA" --modelos ./models/
```

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|------------|
| `--curso` | str | Sim | - | Nome do curso |
| `--modelos` | str | Sim | - | Caminho dos modelos |
| `--output` | str | Não | ./output/previsoes/ | Pasta de saída |

##### Comando: `pipeline`

```bash
python -m cli pipeline --todos-cursos --treinar --prever
```

| Parâmetro | Tipo | Obrigatório | Padrão | Descrição |
|-----------|------|-------------|--------|------------|
| `--todos-cursos` | flag | Não | False | Processar todos os cursos |
| `--treinar` | flag | Não | True | Executar treinamento |
| `--prever` | flag | Não | True | Executar previsão |
| `--campus` | str | Não | FGA | Campus: FGA, UnB |

#### Exemplo de Saída

```
$ python -m cli train --curso "CIENCIA POLITICA"

🔄 Conectando ao banco de dados...
✅ Conexão estabelecida

📊 Carregando dados...
   - Query: sigaa (Treinamento FGA)
   - Alunos carregados: 1,234

🔄 Processando transformação...
   - Situação aplicada: 1,234 registros
   - Tabela pivô: 1,234 alunos × 45 disciplinas

🤖 Treinando modelos para CIENCIA POLITICA / M / 2019.1
   ├── C5.0: F1=0.72 ✓
   ├── Random Forest: F1=0.68 ✗
   ├── RPart: F1=0.71 ✓
   ├── Regressão Logística: F1=0.65 ✗
   └── Rede Neural: F1=0.73 ✓

💾 Modelos salvos: 3 (C5.0, RPart, Rede Neural)
📁 ./models/modelos_treinados_CIENCIA_POLITICA_M_2019_1.joblib
```

#### Fluxo de Execução

```
CLI (main.py)
    │
    ├─► commands/train.py
    │       │
    │       ├─► data_source.connection.connect()
    │       ├─► data_source.queries.QUERY_SIGAA
    │       ├─► transform.situacao.incluir_situacao()
    │       ├─► transform.pivot.montar_tabela()
    │       └─► ml.train.ModelTrainer()
    │
    ├─► commands/predict.py
    │       │
    │       ├─► ml.predict.EvasaoPredictor.carregar_modelos()
    │       ├─► transform.selecionar_alunos_ativos()
    │       └─► ml.predict.executar_previsao()
    │
    └─► commands/pipeline.py
            │ (orquestra train + predict)
```

#### Logging

A CLI configura logging centralizado com:
- Nível: DEBUG (dev) / INFO (produção)
- Output: console + arquivo `output/logs/cli_YYYYMMDD_HHMMSS.log`
- Formato: `%(asctime)s | %(levelname)-8s | %(message)s`

---

## 3. Regras de Negócio a Preservar

| RN | Nome | Descrição | Arquivo Python |
|----|------|-----------|----------------|
| RN-001 | Classificação de Situação | status_discente → FORMADO/EVADIDO | `transform/situacao.py` |
| RN-002 | Validação de Coorte | Coorte válida apenas com FORMADO e EVADIDO | `ml/train.py` |
| RN-003 | Critério de Aceitação | F1-Score >= 0.7 para aceitar modelo | `ml/train.py` |
| RN-004 | Separação por Tipo | Modelos por OB/OBR ou OB+OPT | `ml/train.py` |
| RN-005 | Separação por Campus | Queries por FGA ou UnB | `data_source/queries.py` |
| RN-007 | Exclusão de Cursos | Excluir 'ENGENHARIA' genérico | `data_source/queries.py` |
| RN-008 | Treinamento por Curso | Loop: curso → opção → coorte | `ml/train.py` |
| RN-009 | Previsão Apenas Ativos | Apenas status = ATIVO | `ml/predict.py` |

---

## 4. Dependências Python (requirements.txt)

```txt
# Core
pandas>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
pyyaml>=6.0

# Database
psycopg2-binary>=2.9.0
sqlalchemy>=2.0.0

# ML
scikit-learn>=1.3.0
joblib>=1.3.0

# Dev
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
mypy>=1.5.0
```

---

## 5. Cronograma de Implementação

### Fase 1: Fundação (1 semana)

| Tarefa | Descrição |
|--------|------------|
| 1.1 | Criar estrutura de diretórios |
| 1.2 | Configurar ambiente virtual |
| 1.3 | Criar requirements.txt |
| 1.4 | Criar arquivo .env.example |
| 1.5 | Configurar logging básico |

**Entregáveis:** `requirements.txt`, `.env.example`

---

### Fase 2: Data Source (1-2 semanas)

| Tarefa | Descrição |
|--------|------------|
| 2.1 | Implementar classe `DatabaseConnection` |
| 2.2 | Migrar 10 queries SQL para Python |
| 2.3 | Implementar `execute_query()` |
| 2.4 | Implementar `execute_query_with_params()` |
| 2.5 | Testes unitários |

**Entregáveis:** `src/data_source/connection.py`, `src/data_source/queries.py`
**Specs:** `data_source-conexao.md`, `data_source-queries.md`

---

### Fase 3: Transform (1-2 semanas)

| Tarefa | Descrição |
|--------|------------|
| 3.1 | Implementar `incluir_situacao()` [RN-001] |
| 3.2 | Implementar classe `TabelaPivot` |
| 3.3 | Implementar filtros (selecionar_alunos, etc) |
| 3.4 | Integrar com data_source |
| 3.5 | Testes unitários |

**Entregáveis:** `src/transform/situacao.py`, `src/transform/pivot.py`
**Specs:** `tratamento_dados.md`

---

### Fase 4: ML Treinamento (2-3 semanas)

| Tarefa | Descrição |
|--------|------------|
| 4.1 | Implementar classe `ModelTrainer` |
| 4.2 | Implementar 5 algoritmos (C5, RF, RPart, LogReg, MLP) |
| 4.3 | Implementar validação de coorte [RN-002] |
| 4.4 | Implementar cálculo F1-Score [RN-003] |
| 4.5 | Implementar loop treinamento (curso/opção/coorte) |
| 4.6 | Implementar salvamento de modelos (.joblib) |
| 4.7 | Testes unitários |

**Entregáveis:** `src/ml/train.py`, `models/`
**Specs:** `analise_ml-treinamento.md`

---

### Fase 5: ML Previsão (1 semana)

| Tarefa | Descrição |
|--------|------------|
| 5.1 | Implementar classe `EvasaoPredictor` |
| 5.2 | Implementar `carregar_modelos()` |
| 5.3 | Implementar filtro de ativos [RN-009] |
| 5.4 | Implementar execução de previsão |
| 5.5 | Implementar saída CSV |
| 5.6 | Testes unitários |

**Entregáveis:** `src/ml/predict.py`
**Specs:** `analise_ml-previsao.md`

---

### Fase 6: Integração (1 semana)

| Tarefa | Descrição |
|--------|------------|
| 6.1 | Criar CLI com Click (`src/cli/main.py`) |
| 6.2 | Implementar comando `train` |
| 6.3 | Implementar comando `predict` |
| 6.4 | Implementar comando `pipeline` |
| 6.5 | Configurar logging centralizado |
| 6.6 | Testes de integração |

**Entregáveis:** `src/cli/main.py`, `src/cli/commands/`
**Specs:** Este plano (seção 2.7 CLI)

---

### Fase 7: Qualidade (1 semana)

| Tarefa | Descrição |
|--------|------------|
| 7.1 | Cobertura de testes > 80% |
| 7.2 | Type hints com mypy |
| 7.3 | Formatação com black |
| 7.4 | Documentação (README.md) |

**Entregáveis:** `tests/`, `README.md`

---

## 6. Critérios de Aceitação por Módulo

### Data Source
- [ ] Conexão com PostgreSQL via .env
- [ ] Execução de queries retorna DataFrame
- [ ] Desconexão automática após queries
- [ ] Tratamento de erros de conexão

### Transform
- [ ] `incluir_situacao()` retorna DataFrame com coluna 'situacao'
- [ ] Mapeamento correto: ATIVO-FORMANDO/CONCLUÍDO/Formatura/FORMADO → FORMADO
- [ ] Mapeamento correto: TRANCADO/CANCELADO/DESLIGADO/Transferência → EVADIDO
- [ ] Tabela pivô com linhas=matricula, colunas=codigo_disciplina

### ML Treinamento
- [ ] 5 modelos treinados por coorte
- [ ] F1-Score >= 0.7 para aceitar modelo
- [ ] Modelos salvos em .joblib
- [ ] Métricas registradas em CSV

### ML Previsão
- [ ] Apenas alunos ATIVO são previstos
- [ ] Saída CSV com probabilidade de evasão
- [ ] Log de erros para falhas

---

## 7. Dívidas Técnicas do R Original → Corrigir no Python

### Alta Prioridade
- Credenciais em .env (não hardcoded) — **R: data_source.R:196-200**
- Adicionar testes automatizados

### Média Prioridade
- Remover código duplicado — **R: le_dados/le_dados1**
- Parâmetros configuráveis (não hardcoded)

---

## 8. Referências das Specs

| Spec | Descrição |
|------|------------|
| `sdd/data_source-conexao.md` | Conexão PostgreSQL |
| `sdd/data_source-queries.md` | 10 Queries SQL |
| `sdd/tratamento_dados.md` | Transformação de dados |
| `sdd/analise_ml-treinamento.md` | Treinamento de modelos |
| `sdd/analise_ml-previsao.md` | Previsão de evasão |
| `sdd/etl-pentaho.md` | Pipeline ETL |
| `domain.md` | Regras de negócio |
| `architecture.md` | Arquitetura do sistema |

---

## Resumo Executivo

| Métrica | Valor |
|---------|-------|
| Fases | 7 |
| Duração estimada | 8-10 semanas |
| Módulos principais | 4 |
| Regras de negócio | 8 (RN-001 a RN-009) |
| Specs de referência | 6 SDDs + 2 docs |

---

*Este plano foi baseado na engenharia reversa realizada pelo Reversa em `_reversa_sdd/`*