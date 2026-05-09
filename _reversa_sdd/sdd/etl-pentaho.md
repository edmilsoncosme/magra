# etl-pentaho — Pipeline ETL

## Visão Geral

Pipeline de Extração, Transformação e Carga (ETL) utilizando Pentaho Data Integration (Kettle) para extrair dados dos sistemas acadêmicos SIGAA e SIGRA e carregar na base analítica PostgreSQL. Executado periodicamente para manter os dados atualizados.

## Responsabilidades

- Conectar aos bancos de dados do SIGAA e SIGRA
- Extrair dados de alunos, disciplinas e matriculas
- Aplicar transformações (mapeamento de códigos, joins)
- Carregar dados na base analítica `base_analitica`
- Criar view unificada `alunos_sigaa_sigra_27092022`

## Interface

**Arquivo:** `pentaho/transforms/carregar-dados-analiticos.ktr`

Executado via linha de comando:
```bash
pan.sh -file:pentaho/transforms/carregar-dados-analiticos.ktr
```

### Componentes do ETL

| Componente | Tipo | Descrição |
|------------|------|------------|
| Table Input (SIGAA) | Source | Extrai dados do banco SIGAA |
| Table Input (SIGRA) | Source | Extrai dados do banco SIGRA |
| Table Input (Códigos) | Source | Extrai mapeamento de códigos |
| Select/Rename | Transform | Seleciona e renomeia campos |
| Merge Join | Transform | Faz UNION das fontes |
| Table Output | Sink | Carrega na base analítica |

### Fluxo de Dados

```
SIGAA DB ──► Table Input ──┐
                          ├──► Merge Join ──► Table Output ──► base_analitica
SIGRA DB ──► Table Input ──┘
```

## Regras de Negócio

- Dados extraídos de `base_analitica.sigaa_27092022` e `base_analitica.sigra_27092022` 🟡
- View final une dados de ambas as fontes via UNION ALL 🟢
- Mapeamento de códigos de disciplinas via `base_analitica.codigos_disciplinas_sigaa` 🟡
- Timestamp de extração: 27/09/2022 (hardcoded no nome da view) 🟡

## Fluxo Principal

1. **Input SIGAA**: Ler dados da tabela `sigaa_27092022`
2. **Input SIGRA**: Ler dados da tabela `sigra_27092022`
3. **Input Códigos**: Ler mapeamento de códigos de disciplinas
4. **Transformação**:
   - Selecionar colunas relevantes
   - Renomear campos para padronizar
   - Aplicar filtros necessários
5. **Junção**: UNION ALL das duas fontes
6. **Output**: Inserir na view `alunos_sigaa_sigra_27092022`

### Estrutura da View Resultado

```
colunas: matricula, id_pessoa, sexo, data_nascimento, nacionalidade, raca,
         estado_civil, status_discente, ano_ingresso, periodo_ingresso,
         ano_saiu, nome_curso, periodo_curso, opcao, sigla_campus,
         nome_campus, codigo_comp_curricular, id_disciplina, nome_comp_curricular,
         descricao_tipo_disciplina, cod_dis_sigra, equivalencia_disciplina,
         sigla_dep, nome_dep, tipo_integralizacao, tipo_integralizacao_des,
         conceito, numero_faltas_mc, fonte
```

## Fluxos Alternativos

- **Falha na conexão**: ETL falha, não produz saída 🟡
- **Dados duplicados**: UNION ALL não remove duplicatas (comportamento esperado) 🟢
- **Campo nulo**: mantém NULL na saída 🟢

## Dependências

- **SIGAA** — banco de dados de origem 1 🟢
- **SIGRA** — banco de dados de origem 2 🟢
- **PostgreSQL** — base analítica 🟢

## Requisitos Não Funcionais

| Tipo | Requisito inferido | Evidência no código | Confiança |
|------|--------------------|---------------------|-----------|
| Performance | Extrai ~100k registros em < 5 min | Sem evidência | 🔴 |
| Escalabilidade | Processa crescimento de dados | Sem evidência | 🔴 |
| Disponibilidade | Scheduling via crontab ou Pentaho Server | 🟡 | 🔴 |

## Critérios de Aceitação

```gherkin
Dado que as conexões com SIGAA e SIGRA estão disponíveis
Quando executar o job Pentaho
Então deve extrair dados de ambas as fontes

Dado que os dados foram extraídos
Quando o fluxo de transformação finalizar
Então deve produzir view com UNION de ambas as fontes

Dado que os dados estão prontos para carga
Quando o Table Output executar
Então deve inserir registros na base_analitica

Dado que a conexão com o banco falhar
Quando executar o ETL
Então deve lançar erro e não producir saída
```

## Prioridade

| Requisito | MoSCoW | Justificativa |
|-----------|--------|---------------|
| Extrair do SIGAA | Must | Fonte primária de dados |
| Extrair do SIGRA | Must | Fonte secundária de dados |
| União das fontes | Must | View unificada é consumida pelos R scripts |
| Carregar base analítica | Must | Destino do ETL |
| Logging de erros | Should | Facilita troubleshooting |

## Rastreabilidade de Código

| Arquivo | Componente | Cobertura |
|---------|------------|-----------|
| `pentaho/transforms/carregar-dados-analiticos.ktr` | Transformação Kettle | 🟡 — arquivo binário não analisado |
| `SQL/UNION_SIGAA_SIGRA.sql` | Query de união | 🟢 |

---

**Próximo:** traceability/code-spec-matrix.md. Digite **CONTINUAR** para prosseguir.