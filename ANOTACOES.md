## Prompt para OpenCode
- 01 -  Baseado nas specs de uma engeraria reversa que está na pasta @_reversa_sdd/ foi construido um plano @plano_magra.md de reconstrução de um novo projeto chamado Magra. O objetivo do plano feito é migrar o antigo projeto para Python. Quero que avalie o plano e me informe qual a primeira atividade que deve ser feita.  
- 02 - Recomendação Prévia
Antes de iniciar a implementação, recomendo verificar as specs de conexão e queries em _reversa_sdd/sdd/ para confirmar que estão completas e compreender melhor os filtros SQL obrigatórios mencionados no plano (seção 2.2).

### Sugestão dos próximo passo feito pelo OpenCode
- Próximo passo: criar o módulo transform/situacao.py para classificar FORMADO/EVADIDO RN-001?

### preprando o prompt para o OpenCode
Esotu migrando este projeto que era feito em R e agora estou migrando para Python. 
O plano @plano_magra.md foi definido com base nas especificações que estão na pasta @_reversa_sdd/. 

Seguindo o crongrama do plano, ja foi implementeado a Fase 1 e Fase 2. Sendo que para fazer Fase 2 optei por usar um arquivo .csv @data/raw/fga_20260420.csv que fornecerá os dados brutos, não sendo necessário realizar a implementação das conexões com o Postgres.
A parte de carga desses dados já foi feito no fase 2 do projeto de migração e testada no arquivo @test_loader.py .

Continuando do plano de migração, preciso implementar a "Fase 3: Transform (1-2 semanas)".  


Fase 3: Transform implementada.
Arquivos criados:
Arquivo                     Descrição
src/transform/situacao.py	Função incluir_situacao() (RN-001) - classifica FORMADO/EVADIDO
src/transform/pivot.py	    Classe TabelaPivot + funções de seleção
src/transform/__init__.py	Exports

tests/test_transform.py	25 testes unitários
Para executar os testes:
pip install -r requirements.txt
pytest tests/test_transform.py -v

Uso básico:
from src.data_source import load_csv, apply_standard_filters
from src.transform import incluir_situacao, TabelaPivot, selecionar_alunos
df = load_csv()
df = apply_standard_filters(df)
df = incluir_situacao(df)
df_filtrado = selecionar_alunos(df, nome_curso="CIENCIA POLITICA", opcao="M")
pivot = TabelaPivot().montar(df_filtrado)

## Realizando TESTE 29/25/2026

- Seguindo o crongrama do plano e implementação do projeto magra @_reversa_sdd/plano_magra.md , ja foi implementeado a Fase 1 e Fase 2 e Fase 3. Sendo que para fazer Fase 2 optei por usar um arquivo .csv @data/raw/fga_20260420.csv que fornecerá os dados brutos, não sendo necessário realizar a implementação das conexões com o Postgres.
A parte de carga desses dados já foi feito no fase 2 do projeto de migração e testada no arquivo @test_loader.py.
Para a fase 3, um arquivo de teste unitário foi implementado. Ao executar o teste com o comando "pytest tests/test_transform.py -v", percebo que estão retonrando alguns erros. Verifique que erros são esses e como corrigi-los.

- O prompt acima foi usado para corrigir o erro na montagem da tabela de pivot. 
- Agora será realizado a Fase 4: ML Treinamento (2-3 semanas)

## Prompt para o Antigravity
- Seguindo o crongrama do plano e implementação do projeto magra @_reversa_sdd/plano_magra.md , ja foi implementeado a Fase 1 e Fase 2 e Fase 3. Agora preciso que seja implementado a Fase 4 que é "ML Treinamento (2-3 semanas)". Sendo que para fazer Fase 2 optei por usar um arquivo .csv @data/raw/fga_20260420.csv que fornecerá os dados brutos, não sendo necessário realizar a implementação das conexões com o Postgres. Peço que avalie o plano e me informe qual a primeira atividade que deve ser feita.

### O que foi implementado:

  1. Estrutura Core ( ModelTrainer  em  src/ml/train.py ):
      • Uma classe robusta que gerencia o ciclo de treinamento, desde o recebimento da tabela pivô até a exportação
      final de métricas e persistência dos classificadores aprovados.
  2. Equivalência Algorítmica (Fase 4.2):
      • Migração e mapeamento dos 5 algoritmos de ML do R original para o ecossistema Python moderno ( scikit-learn ):
          • C5.0: Simulado via  AdaBoostClassifier  com estimador de árvore de entropia e 10 trials.
          • Random Forest: Implementado com  RandomForestClassifier  (10 árvores).
          • CART (RPart): Implementado via  DecisionTreeClassifier  com complexidade parametrizada ( ccp_alpha=0.01 ).
          • Regressão Logística: Implementado com  LogisticRegression  de base binomial.
          • Rede Neural: Implementado via  MLPClassifier  com 1 camada oculta de 100 neurônios.

  3. Garantia das Regras de Negócio:
      • RN-002 (Validação de Coorte): Implementada validação que pula automaticamente coortes sem a presença mínima de
      alunos  FORMADO  e  EVADIDO  ou com amostragem insuficiente.
      • RN-003 (Critério de Aceitação): Validação estrita do F1-Score (tendo a evasão como classe de interesse).
      Apenas modelos com $F1 \ge 0.7$ são qualificados para salvamento.
  4. Persistência Estruturada (Fase 4.6):
      • Modelos: Salvamento de dicionários contendo os modelos aprovados e suas respectivas features via  joblib  no
      diretório  /models .
      • Métricas: Consolidação de tabelas de métricas para todas as coortes do curso em formato CSV (separador por
      ponto e vírgula, compatível com a modelagem do R original).
  5. Testes Unitários (Fase 4.7):
      • Criação do arquivo  tests/test_train.py  contendo 11 novos testes detalhados cobrindo:
          • Casos de validação de coorte (vazias, classes únicas, baixo volume).
          • Separação holdout 70/30 (estratificada e simples).
          • Treinamento e avaliação individual de cada um dos 5 classificadores.
          • Fluxo completo de aprovação do threshold e gravação dos arquivos no disco.

### Próxima Etapa:

  Com a base do  ModelTrainer  100% pronta e testada, os próximos passos naturais de acordo com o plano são:

  1. Fase 5: ML Previsão (ML Previsão - 1 semana):
      • Criação da classe  EvasaoPredictor  em  src/ml/predict.py  para carregar os modelos aprovados, filtrar alunos
      com status  ATIVO  e gerar o CSV final com a probabilidade de evasão.
  2. Fase 6: CLI e Integração (1 semana):
      • Criação dos comandos na interface de linha de comando ( train ,  predict  e  pipeline ) para permitir executar
      o treinamento completo a partir dos arquivos  .csv  de dados brutos.


  Como você prefere prosseguir? Gostaria de começar a implementação da Fase 5 (ML Previsão)?          