# Fluxo: data_source (Conexão PostgreSQL)

```mermaid
graph TD
    A[App R] -->|1. chamar| B[conectar]
    B -->|2. dbConnect| C[PostgreSQL localhost:5432]
    C -->|3. retorna| B[connection]
    B -->|4. retorna| D[App]
    
    E[App R] -->|5. chamar| F[le_dados]
    F -->|6. executar| G[dbGetQuery]
    G -->|7. query| C
    C -->|8. dados| G
    G -->|9. dataframe| F
    F -->|10. dbDisconnect| C
    F -->|11. retorna| E[dataframe]

    H[Queries SQL] -->|definidas| F
    style H fill:#f9f,stroke:#333
```

---

## Queries Disponíveis

| Query | Uso |
|-------|-----|
| sigaa | Treinamento FGA - SIGAA |
| sigra | Treinamento FGA - SIGRA |
| sigaa_ativos | Previsão alunos ativos FGA |
| sigaa_sigra_todos | Previsão todos FGA |
| sigaa_sigra_cp | Treinamento Ciência Política |
| sigaa_sigra_cp_todos | Previsão Ciência Política |
| sigaa_sigra_unb | Treinamento UnB (não-FGA) |
| sigaa_sigra_unb_todos | Previsão UnB (não-FGA) |