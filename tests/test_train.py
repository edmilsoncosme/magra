"""Testes unitários para o módulo de treinamento (ModelTrainer)."""

import pytest
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from src.ml.train import ModelTrainer
from sklearn.base import ClassifierMixin


@pytest.fixture
def trainer(tmp_path):
    """Instancia o ModelTrainer apontando as saídas para diretórios temporários."""
    output_dir = tmp_path / "models"
    resultado_dir = tmp_path / "resultados"
    return ModelTrainer(
        output_dir=str(output_dir),
        resultado_dir=str(resultado_dir),
        f1_threshold=0.7,
        random_state=42,
    )


@pytest.fixture
def df_valido():
    """Gera um DataFrame pivô fictício e qualificado para treinamento."""
    np.random.seed(42)
    n_alunos = 20
    disciplinas = ["FGA0168", "FGA0083", "FGA0250", "FGA0003"]

    data = {disc: np.random.choice([0, 1, 2], size=n_alunos) for disc in disciplinas}
    # Adicionar coluna situacao balanceada
    data["situacao"] = ["FORMADO"] * 10 + ["EVADIDO"] * 10

    df = pd.DataFrame(data)
    df.index = [f"matricula_{i}" for i in range(n_alunos)]
    df.index.name = "matricula"
    return df


@pytest.fixture
def df_invalido_uma_classe():
    """Gera um DataFrame pivô com apenas uma classe discente."""
    np.random.seed(42)
    n_alunos = 10
    disciplinas = ["FGA0168", "FGA0083"]

    data = {disc: np.random.choice([0, 1], size=n_alunos) for disc in disciplinas}
    data["situacao"] = ["FORMADO"] * n_alunos

    df = pd.DataFrame(data)
    df.index = [f"matricula_{i}" for i in range(n_alunos)]
    df.index.name = "matricula"
    return df


def test_validar_coorte_nulo_ou_vazio(trainer):
    """Garante que datasets vazios ou nulos são rejeitados."""
    assert trainer.validar_coorte(None) is False
    assert trainer.validar_coorte(pd.DataFrame()) is False


def test_validar_coorte_sem_situacao(trainer):
    """Garante que a ausência do target 'situacao' rejeita o dataset."""
    df = pd.DataFrame({"FGA0168": [1, 2, 0], "FGA0083": [0, 1, 1]})
    assert trainer.validar_coorte(df) is False


def test_validar_coorte_uma_classe(trainer, df_invalido_uma_classe):
    """Garante que coortes com classe única são rejeitadas (RN-002)."""
    assert trainer.validar_coorte(df_invalido_uma_classe) is False


def test_validar_coorte_tamanho_baixo(trainer):
    """Garante que coortes com menos de 4 alunos são rejeitadas."""
    df = pd.DataFrame(
        {"FGA0168": [1, 0, 1], "situacao": ["FORMADO", "EVADIDO", "FORMADO"]}
    )
    assert trainer.validar_coorte(df) is False


def test_validar_coorte_valida(trainer, df_valido):
    """Garante que coortes bem estruturadas são aprovadas para modelagem."""
    assert trainer.validar_coorte(df_valido) is True


def test_split_dados(trainer, df_valido):
    """Verifica a correta separação em features (X) e target (y) na proporção 70/30."""
    X_train, X_test, y_train, y_test = trainer.split_dados(df_valido)

    # 20 instâncias -> 14 treino (70%), 6 teste (30%)
    assert len(X_train) == 14
    assert len(X_test) == 6
    assert len(y_train) == 14
    assert len(y_test) == 6

    # Features não devem conter a coluna target
    assert "situacao" not in X_train.columns
    assert "situacao" not in X_test.columns

    # Garantir que o target mantém o mesmo tipo
    assert isinstance(y_train, pd.Series)
    assert set(y_train.unique()) == {"FORMADO", "EVADIDO"}


def test_treinar_modelos(trainer, df_valido):
    """Testa se cada um dos 5 classificadores do pipeline é treinado e avaliado com sucesso."""
    X_train, X_test, y_train, y_test = trainer.split_dados(df_valido)

    algoritmos = ["C5", "RF", "RPART", "RegLog", "RN"]

    for algo in algoritmos:
        model = trainer.treinar_modelo(algo, X_train, y_train)
        assert isinstance(model, ClassifierMixin)

        f1 = trainer.avaliar_modelo(model, X_test, y_test)
        assert isinstance(f1, float)
        assert 0.0 <= f1 <= 1.0


def test_treinar_modelo_invalido(trainer, df_valido):
    """Garante erro explicativo para algoritmos não suportados."""
    X_train, _, y_train, _ = trainer.split_dados(df_valido)
    with pytest.raises(ValueError, match="Algoritmo desconhecido"):
        trainer.treinar_modelo("XGBoost", X_train, y_train)


def test_treinar_coorte_sem_modelos_aprovados(trainer, df_valido):
    """Verifica o status quando nenhum modelo atinge o limiar F1 desejado."""
    # Seta threshold F1 de 1.1 (impossível de atingir) para forçar rejeição
    trainer.f1_threshold = 1.1

    resultado = trainer.treinar_coorte(
        df_valido,
        curso="CIENCIA POLITICA",
        opcao="M",
        ano=2019,
        periodo=1,
        tipo_integralizacao="OB_OBR",
    )

    assert resultado["status"] == "Sem modelo aceito"
    assert resultado["F1_RF"] != ""
    assert len(list(trainer.output_dir.glob("*.joblib"))) == 0


def test_treinar_coorte_com_sucesso(trainer, df_valido):
    """Valida o fluxo completo de treinamento, aprovação e persistência do modelo."""
    # Seta threshold F1 de 0.0 para garantir que todos os modelos passem
    trainer.f1_threshold = 0.0

    resultado = trainer.treinar_coorte(
        df_valido,
        curso="CIENCIA POLITICA",
        opcao="M",
        ano=2019,
        periodo=1,
        tipo_integralizacao="OB_OBR",
    )

    assert resultado["status"] == "OK"
    assert resultado["F1_RF"] != ""

    # Verifica se o arquivo .joblib foi de fato gravado
    arquivos_salvos = list(trainer.output_dir.glob("*.joblib"))
    assert len(arquivos_salvos) == 1

    # Carrega e valida metadados do joblib
    dados_carregados = joblib.load(arquivos_salvos[0])
    assert dados_carregados["curso"] == "CIENCIA POLITICA"
    assert dados_carregados["opcao"] == "M"
    assert dados_carregados["ano_ingresso"] == 2019
    assert dados_carregados["periodo_ingresso"] == 1
    assert "modelos" in dados_carregados
    assert "RF" in dados_carregados["modelos"]
    assert "features" in dados_carregados["modelos"]["RF"]


def test_registrar_resultados(trainer):
    """Testa a geração consolidada da tabela de métricas em formato CSV."""
    resultados = [
        {
            "opcao": "M",
            "curso": "CIENCIA POLITICA",
            "ano_ingresso": 2019,
            "periodo_ingresso": 1,
            "total_alunos": 20,
            "total_disciplinas": 4,
            "F1_C5O": 0.8,
            "F1_RF": 0.75,
            "F1_RPART": 0.82,
            "F1_RegLog": 0.65,
            "F1_RN": 0.7,
            "tp_integralizacao": "OB_OBR",
            "status": "OK",
        }
    ]

    trainer.registrar_resultados(
        resultados, curso="CIENCIA POLITICA", tipo_integralizacao="OB_OBR"
    )

    arquivos_csv = list(trainer.resultado_dir.glob("*.csv"))
    assert len(arquivos_csv) == 1
    assert "modelo_resultado_ciencia_politica_ob_obr.csv" in arquivos_csv[0].name

    # Ler e validar colunas
    df_lido = pd.read_csv(arquivos_csv[0], sep=";")
    assert len(df_lido) == 1
    assert df_lido.loc[0, "curso"] == "CIENCIA POLITICA"
    assert df_lido.loc[0, "status"] == "OK"
