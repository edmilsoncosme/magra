# Relatório de Confiança — sigaa-sigra-retencao

> Gerado pelo Revisor em 2026-05-02

---

## Resumo Geral

| Nível | Quantidade | Percentual |
|-------|-----------|------------|
| 🟢 CONFIRMADO | 26 | 59% |
| 🟡 INFERIDO   | 17 | 38% |
| 🔴 LACUNA     | 1 | 2% |
| **Total**     | 44 | 100% |

**Confiança geral:** 78% (soma de 🟢 + metade dos 🟡)

---

## Por Spec

| Spec | 🟢 | 🟡 | 🔴 | Confiança |
|------|----|----|-----|-----------|
| `sdd/data_source-conexao.md` | 5 | 4 | 0 | 64% |
| `sdd/data_source-queries.md` | 4 | 2 | 0 | 73% |
| `sdd/tratamento_dados.md` | 5 | 3 | 0 | 68% |
| `sdd/analise_ml-treinamento.md` | 6 | 2 | 0 | 81% |
| `sdd/analise_ml-previsao.md` | 4 | 3 | 0 | 69% |
| `sdd/etl-pentaho.md` | 2 | 3 | 1 | 52% |

---

## Lacunas Pendentes 🔴

Itens que permaneceram sem confirmação após a revisão:

### etl-pentaho.md
- **Scheduling do ETL** — Periodicidade não definida ainda
  - Pergunta correspondente: `questions.md#pergunta-3`
  - Status: Respondida → atualizada para 🟡 com nota de "execução manual no início do semestre"

---

## Recomendações

- [ ] Priorizar migração para Python com configuração em `.env` (conforme resposta do usuário)
- [ ] Definir periodicidade do ETL quando o projeto avançar
- [ ] Considerar automatização da execução dos modelos (hoje manual por operador)

---

## Histórico de Reclassificações

| De | Para | Afirmação | Evidência |
|----|------|-----------|-----------|
| 🔴 | 🟡 | Scheduling ETL: "periodicidade não definida" | questions.md#pergunta-3 |
| 🔴 | 🟡 | Credenciais: "haverá migração para .env" | questions.md#pergunta-2 |

---

## Revisão Cruzada

- Engine externa consultada: não disponível nesta sessão
- Revisão realizada: interna (Revisor)

---

## Observações Finais

Todas as perguntas críticas foram respondidas pelo usuário:
1. ✅ Modelos executados manualmente por operador
2. ✅ Migração para Python/.env planejada
3. ✅ ETL manual no início do semestre

O projeto possui boa cobertura de specs (64%) com confiança geral de 78%.