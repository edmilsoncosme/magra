"""Módulo para criação de tabela pivô de disciplinas por aluno."""

import pandas as pd


class TabelaPivot:
    """Cria tabela pivô aluno x disciplinas para treinamento de modelos ML.

    Transforma dados de formato longo (um registro por disciplina cursada)
    para formato wide (uma linha por aluno, colunas são disciplinas).
    """

    def __init__(self):
        self.pivot_table = None
        self.alunos_processados = None

    def montar(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cria tabela pivô com alunos nas linhas e disciplinas nas colunas.

        Cada célula contém a quantidade de vezes que o aluno cursou a disciplina.

        Args:
            df: DataFrame com colunas 'matricula', 'codigo_comp_curricular' ou 'id_disciplina'

        Returns:
            DataFrame pivô com matricula como índice
        """
        if "matricula" not in df.columns:
            raise ValueError("Coluna 'matricula' não encontrada")

        col_disciplina = (
            "codigo_comp_curricular" if "codigo_comp_curricular" in df.columns else "id_disciplina"
        )

        df_count = df.groupby(["matricula", col_disciplina]).size().reset_index(name="qtd")

        self.pivot_table = df_count.pivot(
            index="matricula", columns=col_disciplina, fill_value=0
        )

        self.alunos_processados = set(self.pivot_table.index)

        return self.pivot_table

    def inserir_contagens(self, df: pd.DataFrame) -> pd.DataFrame:
        """Insere contagens de disciplinas cursadas.

        Args:
            df: DataFrame com dados de disciplinas cursadas

        Returns:
            DataFrame pivô com contagens
        """
        if self.pivot_table is None:
            return self.montar(df)
        return self.pivot_table

    def inserir_situacao(self, df: pd.DataFrame) -> pd.DataFrame:
        """Insere coluna de situação (target) na tabela pivô.

        Args:
            df: DataFrame com coluna 'situacao'

        Returns:
            DataFrame pivô com coluna 'situacao' adicionada
        """
        if self.pivot_table is None:
            raise ValueError("Tabela pivô não foi montada. Execute montar() primeiro.")

        situacao_df = df[["matricula", "situacao"]].drop_duplicates(subset="matricula")

        result = self.pivot_table.copy()
        result["situacao"] = situacao_df.set_index("matricula")["situacao"]

        return result

    def get_disciplinas(self) -> list:
        """Retorna lista de disciplinas na tabela pivô.

        Returns:
            Lista de códigos de disciplinas
        """
        if self.pivot_table is None:
            return []
        return [col for col in self.pivot_table.columns if col != "situacao"]

    def get_alunos(self) -> list:
        """Retorna lista de alunos na tabela pivô.

        Returns:
        """
        if self.pivot_table is None:
            return []
        return list(self.pivot_table.index)


def selecionar_alunos(
    df: pd.DataFrame,
    nome_curso: str | None = None,
    opcao: str | None = None,
    ano_ingresso: int | None = None,
    periodo_ingresso: int | None = None,
) -> pd.DataFrame:
    """Filtra alunos por critérios específicos.

    Args:
        df: DataFrame de entrada
        nome_curso: Nome do curso (opcional)
        opcao: Turno (M/T/N) (opcional)
        ano_ingresso: Ano de ingresso (opcional)
        periodo_ingresso: Período de ingresso (opcional)

    Returns:
        DataFrame filtrado
    """
    result = df.copy()

    if nome_curso is not None:
        result = result[result["nome_curso"] == nome_curso]

    if opcao is not None:
        result = result[result["opcao"] == opcao]

    if ano_ingresso is not None:
        result = result[result["ano_ingresso"] == ano_ingresso]

    if periodo_ingresso is not None:
        result = result[result["periodo_ingresso"] == periodo_ingresso]

    return result


def selecinar_cursos(df: pd.DataFrame, tipo_integralizacao: str | None = None) -> pd.DataFrame:
    """Retorna cursos únicos com opções de integralização.

    Args:
        df: DataFrame de entrada
        tipo_integralizacao: Tipo de integralização (OB/OBR/OPT) (opcional)

    Returns:
        DataFrame com cursos únicos
    """
    cols = ["nome_curso", "opcao"]
    if tipo_integralizacao:
        cols.append("tipo_integralizacao")

    return df[cols].drop_duplicates().sort_values(["nome_curso", "opcao"])


def selecionar_disciplinas_por_opcao(
    df: pd.DataFrame, nome_curso: str, opcao: str, tipo_disciplina: str | None = None
) -> pd.DataFrame:
    """Filtra disciplinas por curso e opção (turno).

    Args:
        df: DataFrame de entrada
        nome_curso: Nome do curso
        opcao: Turno (M/T/N)
        tipo_disciplina: Tipo de disciplina (OB/OBR/OPT) (opcional)

    Returns:
        DataFrame filtrado
    """
    result = df[(df["nome_curso"] == nome_curso) & (df["opcao"] == opcao)]

    if tipo_disciplina:
        result = result[result["tipo_integralizacao"] == tipo_disciplina]

    return result


def selecionar_alunos_ativos(
    df: pd.DataFrame, nome_curso: str | None = None, opcao: str | None = None
) -> pd.DataFrame:
    """Filtra alunos ativos para previsão.

    Args:
        df: DataFrame de entrada
        nome_curso: Nome do curso (opcional)
        opcao: Turno (opcional)

    Returns:
        DataFrame com apenas alunos ativos
    """
    result = df[df["status_discente"] == "ATIVO"]

    if nome_curso:
        result = result[result["nome_curso"] == nome_curso]

    if opcao:
        result = result[result["opcao"] == opcao]

    return result


def selecionar_alunos_ativos_opco(
    df: pd.DataFrame,
    nome_curso: str,
    opcao: str,
    ano_ingresso: int,
    periodo_ingresso: int,
) -> pd.DataFrame:
    """Filtra alunos ativos por curso, opção, ano e período de ingresso.

    Args:
        df: DataFrame de entrada
        nome_curso: Nome do curso
        opcao: Turno (M/T/N)
        ano_ingresso: Ano de ingresso
        periodo_ingresso: Período de ingresso

    Returns:
        DataFrame filtrado
    """
    return df[
        (df["nome_curso"] == nome_curso)
        & (df["opcao"] == opcao)
        & (df["ano_ingresso"] == ano_ingresso)
        & (df["periodo_ingresso"] == periodo_ingresso)
        & (df["status_discente"] == "ATIVO")
    ]