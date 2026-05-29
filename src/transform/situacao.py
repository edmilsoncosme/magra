"""Módulo para classificação de situação de alunos (RN-001)."""

import pandas as pd

FORMADO_STATUS = {"ATIVO - FORMANDO", "CONCLUÍDO", "Formatura", "FORMADO"}
EVADIDO_STATUS = {"TRANCADO", "CANCELADO", "DESLIGADO", "Transferência"}


def incluir_situacao(df: pd.DataFrame) -> pd.DataFrame:
    """Classifica alunos em FORMADO ou EVADIDO com base no status discente.

    RN-001:
    - ATIVO - FORMANDO, CONCLUÍDO, Formatura, FORMADO -> FORMADO
    - TRANCADO, CANCELADO, DESLIGADO, Transferência -> EVADIDO

    Args:
        df: DataFrame com coluna 'status_discente'

    Returns:
        DataFrame com coluna 'situacao' adicionada

    Raises:
        ValueError: Se a coluna 'status_discente' não existir
    """
    if "status_discente" not in df.columns:
        raise ValueError("Coluna 'status_discente' não encontrada no DataFrame")

    df = df.copy()

    def classify(status: str) -> str:
        if status in FORMADO_STATUS:
            return "FORMADO"
        elif status in EVADIDO_STATUS:
            return "EVADIDO"
        else:
            return "EVADIDO"

    df["situacao"] = df["status_discente"].apply(classify)

    return df


def is_valid_coorte(df: pd.DataFrame) -> bool:
    """Verifica se uma coorte tem alunos FORMADOS e EVADIDOS.

    Args:
        df: DataFrame com coluna 'situacao'

    Returns:
        True se a coorte tem ambos os tipos de situação
    """
    if "situacao" not in df.columns:
        return False

    has_formado = (df["situacao"] == "FORMADO").any()
    has_evadido = (df["situacao"] == "EVADIDO").any()

    return bool(has_formado and has_evadido)


def get_situacao_counts(df: pd.DataFrame) -> dict:
    """Retorna contagem de alunos por situação.

    Args:
        df: DataFrame com coluna 'situacao'

    Returns:
        Dicionário com contagens {'FORMADO': int, 'EVADIDO': int}
    """
    if "situacao" not in df.columns:
        return {"FORMADO": 0, "EVADIDO": 0}

    return df["situacao"].value_counts().to_dict()