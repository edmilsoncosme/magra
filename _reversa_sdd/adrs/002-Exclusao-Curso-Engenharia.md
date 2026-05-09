# ADR-002: Exclusão de Registros com Curso "Engenharia" Genérico

## Metadata

- **ID:** ADR-002
- **Título:** Exclusão de Registros com Curso "Engenharia" Genérico
- **Data:** Inferida do código (2022-09)
- **Status:** Aceito ✅
- **Autores:** Edmilson Cosme da Silva

---

## Contexto

As queries SQL do projeto filtram registros onde `nome_curso NOT IN ('ENGENHARIA', 'Engenharia')`.

```
data_source.R:18  - and  nome_curso not in ('ENGENHARIA')
data_source.R:30  - and  nome_curso not in ('Engenharia')
data_source.R:44  - and  nome_curso not in ('ENGENHARIA')
data_source.R:56  - and  nome_curso not in ('ENGENHARIA')
```

---

## Decisão

Excluir de todas as análises registros onde o `nome_curso` contém apenas a palavra "Engenharia" (sem especificação).

---

## Justificativa

1. **Dados incompletos:** O termo "Engenharia" (genérico) parece ser um placeholder para registros sem course específico identificado.

2. **Cursos específicos inclusos:** Há diversos cursos de engenharia específicos que **NÃO** são excluídos:
   - Engenharia de Software
   - Engenharia Ambiental
   - Engenharia de Redes
   - etc.

3. **Padrão consistente:** O filtro aparece em todas as queries, indicando decisão deliberada.

---

## Consequências

### Positivas
- Elimina dados com identificação inconsistente
- Garante que apenas cursos específicos sejam processados

### Negativas
- Pode perder registroslegítimos de cursos de Engenharia não mapeados

---

## Alternativas Consideradas

| Alternativa | Descrição | Motivo de Rejeição |
|-------------|-----------|-------------------|
| Incluir todos | Remover filtro | Manter dados inconsistentes |
| Mapeamento manual | Identificar cursos específicos | Requer conhecimento do domínio |

---

## Confiança

🟡 INFERIDO — Não há documentação explicando o motivo. A hipótese mais provável é dados incompletos/placeholder.