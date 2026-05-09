# Inventário do Projeto — sigaa-sigra-retencao

> Gerado pelo Scout em 2026-05-01

## Estrutura de Pastas

```
raiz/
├── .reversa/                    # Configuração do Reversa (ignorado)
├── .agents/                     # Agentes do Reversa (ignorado)
├── _reversa_sdd/               # Saída do Reversa (ignorado)
├── .git/                        # Repositório Git
│
├── sigaa-sigra-retencao.Rproj   # Projeto R (RStudio)
├── README.md                    # Descrição do projeto
│
├── *.R                          # Scripts R principais
│   ├── tratamento_dados.R      # Funções de tratamento de dados
│   ├── data_source.R           # Conexões e queries PostgreSQL
│   ├── analisar-evasao-sigaa-sigra.R  # Análise e modelos ML
│
├── SQL/                         # Consultas SQL
│   ├── UNION_SIGAA_SIGRA.sql   # União das bases SIGAA e SIGRA
│   ├── DADOS_SIGAA.sql         # Dados do SIGAA
│   ├── DADOS_SIGRA.sql         # Dados do SIGRA
│   ├── PROCEDURE_ATUALIZA_OPCAO_SIGRA.sql
│   └── TESTES_25_09.sql
│
├── pentaho/                     # Transformações ETL (Pentaho)
│   ├── CONFIGURACAO_PENTAHO_WINDOWS.md
│   └── transforms/
│       └── carregar-dados-analiticos.ktr
│
├── tratamento_dados.R          # Funções utilitárias
├── data_source.R               # Conexões PostgreSQL
├── analisar-evasao-sigaa-sigra.R  # Script principal de ML
├── antotações.txt              # Anotações
└── .gitignore
```

---

## Tecnologias Identificadas

| Categoria | Tecnologia | Versão/Notas |
|-----------|------------|--------------|
| **Linguagem** | R | 4.x (via RStudio) |
| **IDE** | RStudio | - |
| **Banco de Dados** | PostgreSQL | Local (localhost:5432) |
| **ETL** | Pentaho | Pentaho Data Integration |

---

## Frameworks e Bibliotecas R

| Biblioteca | Uso |
|------------|-----|
| `tidyverse` | Manipulação de dados (dplyr, tidyr, ggplot2) |
| `RPostgres` | Conexão com PostgreSQL |
| `C50` | Árvore de decisão C5.0 |
| `caTools` | Ferramentas de ML |
| `caret` | Classificação e Regressão |
| `rpart` | Árvores de decisão |
| `rpart.plot` | Visualização de árvores |
| `h2o` | Redes Neurais (Deep Learning) |
| `ranger` | Random Forest |
| `janitor` | Limpeza de dados |
| `stringr` | Manipulação de strings |

---

## Pontos de Entrada

### Scripts Principais

| Script | Função |
|--------|--------|
| `analisar-evasao-sigaa-sigra.R` | Script principal — treina modelos de ML e faz previsões |
| `data_source.R` | Define funções de conexão (`conectar()`, `le_dados()`) |
| `tratamento_dados.R` | Funções de transformação: `incluir_Situacao()`, `montarTabelaDisciplinas()` |

### Banco de Dados

- **Host:** localhost:5432
- **Database:** postgres
- **Usuário:** postgres
- **Senha:** 123456
- **Schema:** base_analitica

### Tabelas do Banco

| Tabela | Descrição |
|--------|-----------|
| `base_analitica.alunos_sigaa_sigra_27092022` | Base unificada de alunos |
| `base_analitica.sigaa_27092022` | Dados do SIGAA |
| `base_analitica.sigra_27092022` | Dados do SIGRA |
| `base_analitica.codigos_disciplinas_sigaa` | Mapeamento de códigos |

---

## Módulos Identificados

### 1. Camada de Dados (`data_source.R`)
- **Responsabilidade:** Conexão e extração de dados do PostgreSQL
- **Interfaces:** Funções `conectar()`, `le_dados()`, `le_dados1()`
- **Dependências:** RPostgres

### 2. Camada de Transformação (`tratamento_dados.R`)
- **Responsabilidade:** Limpeza e transformação de dados acadêmicos
- **Interfaces:** Funções de manipulação de dataframes
- **Dependências:** tidyverse

### 3. Camada de Análise (`analisar-evasao-sigaa-sigra.R`)
- **Responsabilidade:** Modelagem de machine learning e previsão de evasão
- **Interfaces:** Funções `gerar_modelos()`, `realizar_previsao()`
- **Dependências:** C50, h2o, ranger, rpart, caret

### 4. Camada de ETL (`pentaho/`)
- **Responsabilidade:** Extração e carga de dados para o warehouse analítico

### 5. Camada de Queries SQL (`SQL/`)
- **Responsabilidade:** Consultas de extração de dados das tabelas do sistema

---

## Cobertura de Testes

Não foram identificados arquivos de teste no projeto (*.test.*, *.spec.*).

---

## Integrações Externas

| Sistema | Descrição |
|---------|-----------|
| **SIGAA** | Sistema de Gestión Académica (fonte de dados) |
| **SIGRA** | Sistema de Registro Acadêmico (fonte de dados) |
| **Pentaho** | Ferramenta de ETL para Warehouse de dados |

---

## Observações

- Projeto de pesquisa acadêmica (Mestrado — UnB)
- Objetivo: Predição de evasão acadêmica usando técnicas de ML
- Dados do Campus FGA (Faculdade Gamma) e UnB
- Usa coortes (ano/periodo de ingresso) para treinamento de modelos