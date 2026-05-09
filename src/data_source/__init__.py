"""Módulo data_source - Carregamento de dados."""

from .csv_loader import (
    load_csv,
    filter_by_campus,
    filter_by_curso,
    apply_standard_filters,
    get_cursos,
    get_coortes,
)

__all__ = [
    "load_csv",
    "filter_by_campus",
    "filter_by_curso",
    "apply_standard_filters",
    "get_cursos",
    "get_coortes",
]