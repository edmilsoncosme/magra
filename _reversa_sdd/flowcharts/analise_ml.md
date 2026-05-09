# Fluxo: analise_ml (Machine Learning)

## Função: gerar_modelos()

```mermaid
graph TD
    A[gerar_modelos] --> B[conectar base]
    B --> C[para cada curso]
    
    C --> D[selecinarCursos]
    D --> E[para cada opção]
    
    E --> F[para cada coorte]
    F --> G{ambos?}
    G -->|não| F
    G -->|sim| H[montarTabelaDisciplinas]
    
    H --> I[inserirDisplinasCursadas]
    I --> J[inserirSituacaoAluno]
    
    J --> K[treinar C5.0]
    J --> L[treinar Random Forest]
    J --> M[treinar RPart]
    J --> N[treinar Regressão Logística]
    J --> O[treinar Rede Neural]
    
    K --> P{F1 >= 0.7?}
    L --> P
    M --> P
    N --> P
    O --> P
    
    P -->|sim| Q[salvar modelo]
    P -->|não| R[descartar]
    
    Q --> S[gravar CSV métricas]
    R --> F
    
    S --> T[arquivos/modelos/]
    
    style Q fill:#9f9,stroke:#333
    style T fill:#f9f,stroke:#333
```

---

## Função: realizar_previsao()

```mermaid
graph TD
    A[realizar_previsao] --> B[carregar modelos]
    B --> C[para cada curso]
    
    C --> D[carregar arquivo .Rdata]
    D --> E[para cada modelo]
    
    E --> F[selecionar alunos ativos]
    F --> G[montarTabelaDisciplinas]
    G --> H[prever situacao]
    
    H --> I{EVADIDO?}
    I -->|sim| J[adicionar à lista]
    I -->|não| K[ignorar]
    
    J --> L[exportar CSV]
    L --> M[arquivos/previsoes/]
    
    K --> E
    
    style J fill:#ff9,stroke:#333
    style M fill:#f9f,stroke:#333
```

---

## Modelos e Métricas

| Modelo | Biblioteca | Métrica |
|--------|------------|---------|
| C5.0 | C50 | F1-Score (byClass[7]) |
| Random Forest | ranger | F1-Score |
| RPart | rpart | F1-Score |
| Regressão Logística | glm | F1-Score |
| Rede Neural | h2o | F1-Score |

**Threshold:** F1 >= 0.7 para aceitar modelo