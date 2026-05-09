# MAGRA - Modelo de Análise na Graduação

Este projeto implementa um sistema completo para previsão de evasão de estudantes universitários, com foco na aplicação prática e reutilização de código. O sistema segue uma arquitetura modular, separa clara responsabilidades e oferece uma interface de linha de comando (CLI) para operação.

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd magra
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   # Windows:
   python -m venv venv
   venv\Scripts\activate
   # Linux com python 3.13:
   sudo apt install python3.13-venv
   python3.13 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure a conexão com o banco de dados:
   Edite o arquivo `src/data_source/config.py` e configure as credenciais do banco SIGAA.

## 📋 Requisitos do Projeto

O projeto deve atender aos seguintes requisitos arquiteturais:

### 1. Estrutura de Arquivos
```
magra/
├── src/
│   ├── data_source/       # Camada de dados
│   │   ├── __init__.py
│   │   ├── connection.py    # connect() → conexao
│   │   ├── queries.py       #QUERY_SIGAA (const)
│   │   └── config.py        # Credenciais
│   ├── transform/           # Transformações
│   │   ├── __init__.py
│   │   ├── situacao.py      # incluir_situacao()
│   │   ├── pivot.py         # montar_tabela()
│   │   └── selection.py     # selecionar_alunos_ativos()
│   ├── ml/                  # Machine Learning
│   │   ├── __init__.py
│   │   ├── train.py         # ModelTrainer
│   │   └── predict.py       # EvasaoPredictor
│   ├── cli/                 # Interface de Linha de Comando
│   │   ├── __init__.py
│   │   ├── main.py          # Entry point (Click)
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── train.py     # Comando: train
│   │       ├── predict.py   # Comando: predict
│   │       └── pipeline.py  # Pipeline completo
│   ├── utils/               # Utilidades
│   └── main.py              # Script executável
├── data/
│   ├── entrada/
│   └── saida/
├── models/                  # Modelos treinados
├── output/                  # Logs, previsões, etc.
├── notebooks/               # Jupyter notebooks
└── README.md                # Documentação
```

### 2. Camadas de Código

#### 2.1 data_source
- `connect.py`: Função `connect()` retorna conexão com banco de dados.
- `queries.py`: Constante `QUERY_SIGAA` com query SQL para alunos.
- `config.py`: Configuração de conexão.

#### 2.2 transform
- `situacao.py`: Função `incluir_situacao()` aplicaRN-1.
- `pivot.py`: Função `montar_tabela()` aplica RN-2.
- `selection.py`: Função `selecionar_alunos_ativos()` aplica RN-3.

#### 2.3 ml
- `train.py`: Classe `ModelTrainer` com `train_models()`.
  - Treina C5.0, Random Forest, RPart, RegLog, Neural Net.
  - Salva modelos em arquivo `.joblib`.
- `predict.py`: Classe `EvasaoPredictor` com `executar_previsao()`.

#### 2.4 cli → Interface de Linha de Comando

Estrutura:
```
src/cli/
├── __init__.py           # Package marker
├── main.py               # Entry point (Click)
├── commands/
│   ├── __init__.py       # Package marker
│   ├── train.py          # Comando: treinar modelos
│   ├── predict.py        # Comando: executar previsões
│   └── pipeline.py       # Comando: pipeline completo
└── options.py            # Argumentos compartilhados
```

Dependências:
```python
click>=8.1.0      # Framework CLI
rich>=13.0.0      # Output formatado (opcional)
```

Comandos Disponíveis:

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

Exemplo de Saída:

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

Fluxo de Execução:

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
    │       └─► ml