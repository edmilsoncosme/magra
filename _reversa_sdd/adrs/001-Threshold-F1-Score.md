# ADR-001: Threshold de F1-Score >= 0.7 para Modelos Preditivos

## Metadata

- **ID:** ADR-001
- **Título:** Threshold de F1-Score >= 0.7 para Modelos Preditivos
- **Data:** Inferida do código (2022-09)
- **Status:** Aceito ✅
- **Autores:** Edmilson Cosme da Silva

---

## Contexto

O sistema de predição de evasão acadêmica tem como objetivo identificar alunos em risco de evasão para que ações preventivas possam ser tomadas. Um modelo preditivo com baixa precisão geraria:
- Alertas falsos positivos (aluno warned indevidamente)
- Alertas falsos negativos (aluno em risco não identificado)
- Desperdício de recursos em intervenções desnecessárias

---

## Decisão

Um modelo preditivo é **aceito** apenas se seu **F1-Score >= 0.7 (70%)**.

O F1-Score é calculado via `confusionMatrix()` do pacote `caret`, utilizando a classe positiva como referência.

---

## Justificativa

1. **Balanço precisão/recall:** F1-Score é a média harmônica de precisão e recall, adequado para dados desbalanceados.

2. **Threshold da literatura:** 0.7 (70%) é um threshold comum em problemas de classificação binária.

3. **Com base no código:** Encontrado em múltiplas linhas do `analisar-evasao-sigaa-sigra.R`:
   - Linha 177: `if (!is.na(F1_C5O) & F1_C5O >= 0.7)`
   - Linha 227: `if (!is.na(F1_RF) & F1_RF >= 0.7)`
   - Linha 266: `if (!is.na(F1_RPART) & F1_RPART >= 0.7)`
   - Linha 308: `if (!is.na(F1_RegLog) & F1_RegLog >= 0.7)`
   - Linha 349: `if (!is.na(F1_RN) & F1_RN >= 0.7)`

---

## Consequências

### Positivas
- Modelos com alta precisão são deployed
- Menor custo com falsos alertas
- Maior confiança nas previsões

### Negativas
- Muitas coortes são rejeitadas (apenas ~30% aceitas segundo logs)
- Alto custo computacional para baixo retorno inicial
- Alguns cursos podem nunca gerar modelos válidos

---

## Alternativas Consideradas

| Alternativa | Descrição | Motivo de Rejeição |
|-------------|-----------|-------------------|
| F1 >= 0.5 | Threshold mais baixo | Gera muitos falsos positivos |
| Acurácia >= 0.8 | Métrica mais simples | Ignora desbalanceamento |
| AUC >= 0.8 | Área sob curva | Requer cálculo adicional |

---

## Referências

- Código: `analisar-evasao-sigaa-sigra.R`
- Biblioteca: `caret::confusionMatrix()`
- Commit histórico: `4f25547` — "Houveram várias correções"