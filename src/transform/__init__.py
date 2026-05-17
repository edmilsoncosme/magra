"""Módulo transform - Transformação de dados para ML."""

from .situacao import incluir_situacao, is_valid_coorte, get_situacao_counts
from .pivot import (
    TabelaPivot,
    selecionar_alunos,
    selecinar_cursos,
    selecionar_disciplinas_por_opcao,
    selecionar_alunos_ativos,
    selecionar_alunos_ativos_opco,
)

__all__ = [
    "incluir_situacao",
    "is_valid_coorte",
    "get_situacao_counts",
    "TabelaPivot",
    "selecionar_alunos",
    "selecinar_cursos",
    "selecionar_disciplinas_por_opcao",
    "selecionar_alunos_ativos",
    "selecionar_alunos_ativos_opco",
]