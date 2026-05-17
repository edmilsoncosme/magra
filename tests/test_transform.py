"""Testes unitários para o módulo transform."""

import pandas as pd
import pytest
from src.transform.situacao import incluir_situacao, is_valid_coorte, get_situacao_counts
from src.transform.pivot import (
    TabelaPivot,
    selecionar_alunos,
    selecinar_cursos,
    selecionar_alunos_ativos,
)


class TestIncluirSituacao:
    """Testes para a função incluir_situacao (RN-001)."""

    def test_concluido_formado(self):
        """Testa que CONCLUÍDO -> FORMADO."""
        df = pd.DataFrame({"status_discente": ["CONCLUÍDO"]})
        result = incluir_situacao(df)
        assert result.loc[0, "situacao"] == "FORMADO"

    def test_ativo_formando_formado(self):
        """Testa que ATIVO - FORMANDO -> FORMADO."""
        df = pd.DataFrame({"status_discente": ["ATIVO - FORMANDO"]})
        result = incluir_situacao(df)
        assert result.loc[0, "situacao"] == "FORMADO"

    def test_formatura_formado(self):
        """Testa que Formatura -> FORMADO."""
        df = pd.DataFrame({"status_discente": ["Formatura"]})
        result = incluir_situacao(df)
        assert result.loc[0, "situacao"] == "FORMADO"

    def test_formado_maiusculo_formado(self):
        """Testa que FORMADO -> FORMADO."""
        df = pd.DataFrame({"status_discente": ["FORMADO"]})
        result = incluir_situacao(df)
        assert result.loc[0, "situacao"] == "FORMADO"

    def test_trancado_evadido(self):
        """Testa que TRANCADO -> EVADIDO."""
        df = pd.DataFrame({"status_discente": ["TRANCADO"]})
        result = incluir_situacao(df)
        assert result.loc[0, "situacao"] == "EVADIDO"

    def test_cancelado_evadido(self):
        """Testa que CANCELADO -> EVADIDO."""
        df = pd.DataFrame({"status_discente": ["CANCELADO"]})
        result = incluir_situacao(df)
        assert result.loc[0, "situacao"] == "EVADIDO"

    def test_desligado_evadido(self):
        """Testa que DESLIGADO -> EVADIDO."""
        df = pd.DataFrame({"status_discente": ["DESLIGADO"]})
        result = incluir_situacao(df)
        assert result.loc[0, "situacao"] == "EVADIDO"

    def test_transferencia_evadido(self):
        """Testa que Transferência -> EVADIDO."""
        df = pd.DataFrame({"status_discente": ["Transferência"]})
        result = incluir_situacao(df)
        assert result.loc[0, "situacao"] == "EVADIDO"

    def test_mixed_statuses(self):
        """Testa múltiplos status diferentes."""
        df = pd.DataFrame(
            {
                "status_discente": [
                    "CONCLUÍDO",
                    "TRANCADO",
                    "ATIVO - FORMANDO",
                    "CANCELADO",
                ]
            }
        )
        result = incluir_situacao(df)
        assert result.loc[0, "situacao"] == "FORMADO"
        assert result.loc[1, "situacao"] == "EVADIDO"
        assert result.loc[2, "situacao"] == "FORMADO"
        assert result.loc[3, "situacao"] == "EVADIDO"

    def test_unknown_status_evadido(self):
        """Testa que status desconhecido -> EVADIDO."""
        df = pd.DataFrame({"status_discente": ["STATUS_DESCONHECIDO"]})
        result = incluir_situacao(df)
        assert result.loc[0, "situacao"] == "EVADIDO"

    def test_missing_column_raises_error(self):
        """Testa que erro é lançado se coluna não existe."""
        df = pd.DataFrame({"outra_coluna": ["valor"]})
        with pytest.raises(ValueError, match="status_discente"):
            incluir_situacao(df)

    def test_preserves_other_columns(self):
        """Testa que outras colunas são preservadas."""
        df = pd.DataFrame(
            {"status_discente": ["CONCLUÍDO"], "matricula": [123], "nome": ["Aluno"]}
        )
        result = incluir_situacao(df)
        assert "matricula" in result.columns
        assert "nome" in result.columns
        assert result.loc[0, "matricula"] == 123


class TestIsValidCoorte:
    """Testes para a função is_valid_coorte."""

    def test_valid_coorte(self):
        """Testa coorte com ambos FORMADO e EVADIDO."""
        df = pd.DataFrame({"situacao": ["FORMADO", "EVADIDO", "FORMADO"]})
        assert is_valid_coorte(df) is True

    def test_only_formado(self):
        """Testa coorte apenas com FORMADO."""
        df = pd.DataFrame({"situacao": ["FORMADO", "FORMADO"]})
        assert is_valid_coorte(df) is False

    def test_only_evadido(self):
        """Testa coorte apenas com EVADIDO."""
        df = pd.DataFrame({"situacao": ["EVADIDO", "EVADIDO"]})
        assert is_valid_coorte(df) is False

    def test_empty_dataframe(self):
        """Testa DataFrame vazio."""
        df = pd.DataFrame({"situacao": []})
        assert is_valid_coorte(df) is False


class TestGetSituacaoCounts:
    """Testes para a função get_situacao_counts."""

    def test_counts(self):
        """Testa contagem de situações."""
        df = pd.DataFrame(
            {"situacao": ["FORMADO", "FORMADO", "EVADIDO", "FORMADO", "EVADIDO"]}
        )
        counts = get_situacao_counts(df)
        assert counts["FORMADO"] == 3
        assert counts["EVADIDO"] == 2


class TestTabelaPivot:
    """Testes para a classe TabelaPivot."""

    def test_montar_pivot(self):
        """Testa criação de tabela pivô."""
        df = pd.DataFrame(
            {
                "matricula": [1, 1, 2, 2, 3],
                "codigo_comp_curricular": ["A", "B", "A", "C", "A"],
            }
        )
        pivot = TabelaPivot()
        result = pivot.montar(df)

        assert result.loc[1, "A"] == 1
        assert result.loc[1, "B"] == 1
        assert result.loc[2, "A"] == 1
        assert result.loc[2, "C"] == 1
        assert result.loc[3, "A"] == 1

    def test_montar_sem_coluna_raises_error(self):
        """Testa erro quando coluna não existe."""
        df = pd.DataFrame({"outra_coluna": [1]})
        pivot = TabelaPivot()
        with pytest.raises(ValueError, match="matricula"):
            pivot.montar(df)

    def test_get_disciplinas(self):
        """Testa getter de disciplinas."""
        df = pd.DataFrame(
            {"matricula": [1, 2], "codigo_comp_curricular": ["A", "B"]}
        )
        pivot = TabelaPivot()
        pivot.montar(df)
        disciplinas = pivot.get_disciplinas()
        assert "A" in disciplinas
        assert "B" in disciplinas


class TestSelecionarAlunos:
    """Testes para funções de seleção."""

    def test_selecionar_por_curso(self):
        """Testa seleção por curso."""
        df = pd.DataFrame(
            {
                "nome_curso": ["ENGENHARIA", "CIENCIA POLITICA", "ENGENHARIA"],
                "matricula": [1, 2, 3],
            }
        )
        result = selecionar_alunos(df, nome_curso="CIENCIA POLITICA")
        assert len(result) == 1
        assert result.iloc[0]["nome_curso"] == "CIENCIA POLITICA"

    def test_selecionar_por_curso_e_opcao(self):
        """Testa seleção por curso e opção."""
        df = pd.DataFrame(
            {
                "nome_curso": ["CIENCIA POLITICA", "CIENCIA POLITICA"],
                "opcao": ["M", "T"],
                "matricula": [1, 2],
            }
        )
        result = selecionar_alunos(df, nome_curso="CIENCIA POLITICA", opcao="M")
        assert len(result) == 1
        assert result.iloc[0]["opcao"] == "M"

    def test_selecionar_por_coorte(self):
        """Testa seleção por coorte."""
        df = pd.DataFrame(
            {
                "ano_ingresso": [2019, 2019, 2020],
                "periodo_ingresso": [1, 1, 1],
                "matricula": [1, 2, 3],
            }
        )
        result = selecionar_alunos(df, ano_ingresso=2019, periodo_ingresso=1)
        assert len(result) == 2


class TestSelecionarAlunosAtivos:
    """Testes para seleção de alunos ativos."""

    def test_filtra_ativos(self):
        """Testa que apenas ativos são retornados."""
        df = pd.DataFrame(
            {
                "status_discente": ["ATIVO", "ATIVO", "TRANCADO", "CONCLUÍDO"],
                "matricula": [1, 2, 3, 4],
            }
        )
        result = selecionar_alunos_ativos(df)
        assert len(result) == 2
        assert all(result["status_discente"] == "ATIVO")

    def test_filtra_ativos_por_curso(self):
        """Testa ativos com filtro de curso."""
        df = pd.DataFrame(
            {
                "nome_curso": ["CIENCIA POLITICA", "CIENCIA POLITICA", "DIREITO"],
                "status_discente": ["ATIVO", "ATIVO", "ATIVO"],
                "matricula": [1, 2, 3],
            }
        )
        result = selecionar_alunos_ativos(df, nome_curso="CIENCIA POLITICA")
        assert len(result) == 2