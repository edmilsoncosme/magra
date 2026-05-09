# Perguntas para Validação — sigaa-sigra-retencao

> Gerado pelo Revisor em 2026-05-02
> Responda cada pergunta e me avise quando terminar.

---

## Pergunta 1 ✅ Respondida

**Contexto:** Módulo `analise_ml-treinamento.md` — modelos treinados são salvos em arquivos `.Rdata`
**Spec afetada:** [`_reversa_sdd/sdd/analise_ml-treinamento.md`], [`_reversa_sdd/sdd/analise_ml-previsao.md`]
**Pergunta:** Como os modelos treinados são disponibilizados para uso? Há uma API, um scheduler, ou são executados manualmente por um operador?
**Impacto:** Se houver um sistema de deployment ou API, preciso adicionar essa integração à spec e ao diagrama C4.

**Resposta:** Os modelos são executados manualmente por um operador.

---

## Pergunta 2 ✅ Respondida

**Contexto:** Módulo `data_source-conexao.md` — credenciais hardcoded (postgres/123456)
**Spec afetada:** [`_reversa_sdd/sdd/data_source-conexao.md`]
**Pergunta:** Existe algum plano de migrar as credenciais para um arquivo de configuração externo (`.env`, `config.yml`) ou vault?
**Impacto:** Se houver plano, marco como 🟡 com nota. Se não houver, mantenho como dívida técnica crítica (🔴).

**Resposta:** Sim, existe a intenção de migrar esse projeto para Python, desta forma as credenciais serão migradas para o arquivo .env.

---

## Pergunta 3 ✅ Respondida

**Contexto:** Módulo `etl-pentaho.md` — scheduling do ETL
**Spec afetada:** [`_reversa_sdd/sdd/etl-pentaho.md`]
**Pergunta:** O ETL é executado periodicamente? Se sim, qual a frequência (diária, semanal)? Usa crontab, Pentaho Server, ou outro scheduler?
**Impacto:** A spec precisa incluir informações de scheduling e dependências.

**Resposta:** Ainda não foi definida a periodicidade da execução do ETL. Nesta fase do projeto foi executado manualmente no início do semestre letivo.