"""Módulo para carregamento de dados CSV."""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "raw"


def load_csv(filename: str = "fga_20260420.csv") -> pd.DataFrame:
    """Carrega dados de um arquivo CSV.

    Args:
        filename: Nome do arquivo CSV em data/raw/

    Returns:
        DataFrame com os dados carregados
    """
    filepath = DATA_DIR / filename
    return pd.read_csv(filepath, sep=";")


def filter_by_campus(df: pd.DataFrame, campus: str) -> pd.DataFrame:
    """Filtra dados por campus.

    Args:
        df: DataFrame de entrada
        campus: Sigla do campus (FGA, UnB, etc)

    Returns:
        DataFrame filtrado
    """
    return df[df["sigla_campus"] == campus]


def filter_by_curso(df: pd.DataFrame, curso: str) -> pd.DataFrame:
    """Filtra dados por curso.

    Args:
        df: DataFrame de entrada
        curso: Nome do curso

    Returns:
        DataFrame filtrado
    """
    return df[df["nome_curso"] == curso]


def filter_exclude_engenharia(df: pd.DataFrame) -> pd.DataFrame:
    """Exclui registros com curso genérico 'ENGENHARIA'.

    Args:
        df: DataFrame de entrada

    Returns:
        DataFrame sem cursos 'ENGENHARIA'
    """
    return df[~df["nome_curso"].isin(["ENGENHARIA", "Engenharia"])]


def filter_disciplinas(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra apenas registros do tipo 'DISCIPLINA'.

    Args:
        df: DataFrame de entrada

    Returns:
        DataFrame apenas com disciplinas
    """
    return df[df["descricao_tipo_disciplina"] == "DISCIPLINA"]


def filter_conceito_not_null(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra registros com conceito não nulo.

    Args:
        df: DataFrame de entrada

    Returns:
        DataFrame apenas com conceito não nulo
    """
    return df[df["conceito"].notna()]


def apply_standard_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica filtros padrão equivalentes às queries SQL do sistema legado.

    Filtros aplicados:
    - Exclusão de cursos genéricos 'ENGENHARIA'
    - Apenas tipo 'DISCIPLINA'
    - Conceito não nulo

    Args:
        df: DataFrame de entrada

    Returns:
        DataFrame com filtros aplicados
    """
    return (
        df.pipe(filter_exclude_engenharia)
        .pipe(filter_disciplinas)
        .pipe(filter_conceito_not_null)
    )


def get_cursos(df: pd.DataFrame) -> list[str]:
    """Retorna lista de cursos únicos.

    Args:
        df: DataFrame de entrada

    Returns:
        Lista de nomes de cursos únicos
    """
    return sorted(df["nome_curso"].unique())


def get_coortes(df: pd.DataFrame) -> list[tuple[int, int]]:
    """Retorna lista de coortes únicas (ano, período).

    Args:
        df: DataFrame de entrada

    Returns:
        Lista de tuplas (ano_ingresso, periodo_ingresso)
    """
    coortes = df[["ano_ingresso", "periodo_ingresso"]].drop_duplicates()
    return sorted(zip(coortes["ano_ingresso"], coortes["periodo_ingresso"]))