"""Módulo de treinamento de modelos de Machine Learning (Fase 4)."""

import logging
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score
import joblib
from src.config import get_logger

logger = get_logger("magra")


class ModelTrainer:
    """Orquestra o treinamento, validação e persistência dos modelos preditivos."""

    def __init__(
        self,
        output_dir: str = "./models",
        resultado_dir: str = "./output/resultados",
        f1_threshold: float = 0.7,
        random_state: int = 42,
    ):
        """Inicializa o ModelTrainer.

        Args:
            output_dir: Pasta onde os modelos .joblib serão salvos
            resultado_dir: Pasta onde as métricas em CSV serão salvas
            f1_threshold: Limiar de F1-Score para aceitação e salvamento do modelo
            random_state: Semente de aleatoriedade para reprodutibilidade
        """
        self.output_dir = Path(output_dir)
        self.resultado_dir = Path(resultado_dir)
        self.f1_threshold = f1_threshold
        self.random_state = random_state

        # Garantir que as pastas existam
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.resultado_dir.mkdir(parents=True, exist_ok=True)

    def validar_coorte(self, df_pivot: pd.DataFrame) -> bool:
        """Verifica se a coorte é válida para modelagem (RN-002).

        Uma coorte é válida apenas se contiver registros de ambas as situações:
        FORMADO e EVADIDO. Também exige um tamanho mínimo de dados para treino.

        Args:
            df_pivot: Tabela pivô contendo a coluna 'situacao'

        Returns:
            True se a coorte for válida, False caso contrário
        """
        if df_pivot is None or df_pivot.empty:
            logger.warning("Dataset vazio ou nulo recebido para validação.")
            return False

        if "situacao" not in df_pivot.columns:
            logger.warning("Coluna 'situacao' não encontrada no DataFrame.")
            return False

        classes = df_pivot["situacao"].unique()
        if len(classes) < 2:
            logger.info(
                f"Coorte rejeitada (RN-002): apenas uma classe presente: {classes}."
            )
            return False

        # Verifica se ambas as classes obrigatórias estão de fato representadas
        counts = df_pivot["situacao"].value_counts()
        if "FORMADO" not in counts or "EVADIDO" not in counts:
            logger.info(
                f"Coorte rejeitada (RN-002): classes obrigatórias incompletas. Contagens: {counts.to_dict()}."
            )
            return False

        # Validação adicional contra datasets excessivamente pequenos
        total_alunos = len(df_pivot)
        if total_alunos < 4:
            logger.info(
                f"Coorte rejeitada: número de alunos muito baixo para treinamento ({total_alunos} alunos)."
            )
            return False

        return True

    def split_dados(
        self, df_pivot: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Divide o dataset em treino e teste (70/30) com holdout.

        Se houver pelo menos 2 instâncias de cada classe, realiza a divisão estratificada
        para manter a proporção da variável target 'situacao' em ambas as bases.

        Args:
            df_pivot: Tabela pivô contendo a coluna 'situacao'

        Returns:
            X_train, X_test, y_train, y_test
        """
        X = df_pivot.drop(columns=["situacao"])
        y = df_pivot["situacao"]

        counts = y.value_counts()
        pode_estratificar = counts.min() >= 2

        if pode_estratificar:
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.3,
                stratify=y,
                random_state=self.random_state,
            )
        else:
            logger.warning(
                f"Tamanho de classe muito pequeno para estratificação ({counts.to_dict()}). Realizando split simples."
            )
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.3,
                random_state=self.random_state,
            )

        return X_train, X_test, y_train, y_test

    def treinar_modelo(
        self, model_name: str, X_train: pd.DataFrame, y_train: pd.Series
    ) -> object:
        """Instancia e treina um dos 5 classificadores do pipeline.

        Modelos implementados:
        - C5: AdaBoostClassifier com árvore de decisão e 10 trials
        - RF: RandomForestClassifier com 10 árvores
        - RPART: DecisionTreeClassifier com cp (ccp_alpha) = 0.01
        - RegLog: LogisticRegression binomial
        - RN: MLPClassifier Rede Neural com 1 camada oculta de 100 neurônios

        Args:
            model_name: Nome do algoritmo ('C5', 'RF', 'RPART', 'RegLog', 'RN')
            X_train: Features de treinamento
            y_train: Target de treinamento

        Returns:
            Modelo treinado

        Raises:
            ValueError: Se o modelo solicitado for desconhecido
        """
        if model_name == "C5":
            # Equivalente ao C5.0 do R com trials=10
            base = DecisionTreeClassifier(
                criterion="entropy", random_state=self.random_state
            )
            model = AdaBoostClassifier(
                estimator=base, n_estimators=10, random_state=self.random_state
            )
        elif model_name == "RF":
            # Equivalente ao Random Forest ranger com num.trees=10
            model = RandomForestClassifier(
                n_estimators=10, random_state=self.random_state
            )
        elif model_name == "RPART":
            # Equivalente ao RPart CART com cp=0.01
            model = DecisionTreeClassifier(
                ccp_alpha=0.01, random_state=self.random_state
            )
        elif model_name == "RegLog":
            # Equivalente ao glm binomial
            model = LogisticRegression(
                max_iter=1000, random_state=self.random_state
            )
        elif model_name == "RN":
            # Equivalente ao h2o.deeplearning neural network
            model = MLPClassifier(
                hidden_layer_sizes=(100,),
                max_iter=1000,
                random_state=self.random_state,
            )
        else:
            raise ValueError(f"Algoritmo desconhecido: {model_name}")

        model.fit(X_train, y_train)
        return model

    def avaliar_modelo(
        self, model: object, X_test: pd.DataFrame, y_test: pd.Series
    ) -> float:
        """Avalia o modelo calculando o F1-Score para a classe 'EVADIDO' (RN-003).

        Args:
            model: Modelo treinado
            X_test: Features de teste
            y_test: Target de teste

        Returns:
            F1-score calculado, ou 0.0 em caso de erro na métrica
        """
        y_pred = model.predict(X_test)

        # F1-Score do caret no R padrão foca na primeira classe (ordem alfabética 'EVADIDO')
        # como nossa classe de interesse principal para prever retenção escolar.
        f1 = f1_score(
            y_test,
            y_pred,
            pos_label="EVADIDO",
            average="binary",
            zero_division=0.0,
        )
        return float(f1)

    def treinar_coorte(
        self,
        df_pivot: pd.DataFrame,
        curso: str,
        opcao: str,
        ano: int,
        periodo: int,
        tipo_integralizacao: str = "OB_OBR",
    ) -> dict:
        """Executa a validação, divisão, treino e avaliação de uma coorte específica.

        Modelos aprovados que atingirem o threshold de F1-Score >= 0.7
        são guardados em disco em arquivo .joblib.

        Args:
            df_pivot: Tabela pivô com features e coluna 'situacao'
            curso: Nome do curso
            opcao: Código/turno da opção
            ano: Ano de ingresso da coorte
            periodo: Período de ingresso da coorte
            tipo_integralizacao: String de integralização para o log/registro

        Returns:
            Dicionário com o resultado do andamento do treinamento
        """
        coorte_str = f"{ano}.{periodo}"
        logger.info(
            f"Iniciando treinamento: {curso} | Opção: {opcao} | Coorte: {coorte_str}"
        )

        resultado_registro = {
            "opcao": opcao,
            "curso": curso,
            "ano_ingresso": ano,
            "periodo_ingresso": periodo,
            "total_alunos": len(df_pivot) if df_pivot is not None else 0,
            "total_disciplinas": (
                len(df_pivot.columns) - 1 if df_pivot is not None else 0
            ),
            "F1_C5O": "",
            "F1_RF": "",
            "F1_RPART": "",
            "F1_RegLog": "",
            "F1_RN": "",
            "tp_integralizacao": tipo_integralizacao,
            "status": "Iniciado",
        }

        # 1. Validação de Coorte (RN-002)
        if not self.validar_coorte(df_pivot):
            msg = "Rejeitado (Classes insuficientes)"
            logger.warning(
                f"Coorte {curso} {opcao} {coorte_str} não qualificada para ML: {msg}"
            )
            resultado_registro["status"] = "Erro de classe"
            return resultado_registro

        # 2. Divisão Holdout 70/30
        X_train, X_test, y_train, y_test = self.split_dados(df_pivot)

        modelos_nomes = {
            "C5": "F1_C5O",
            "RF": "F1_RF",
            "RPART": "F1_RPART",
            "RegLog": "F1_RegLog",
            "RN": "F1_RN",
        }

        modelos_aprovados = {}

        # 3. Treinar e Avaliar cada modelo
        for key, res_col in modelos_nomes.items():
            try:
                model = self.treinar_modelo(key, X_train, y_train)
                f1 = self.avaliar_modelo(model, X_test, y_test)
                resultado_registro[res_col] = round(f1, 4)

                logger.info(f"Modelo {key} treinado para {coorte_str}. F1: {f1:.4f}")

                # Critério de Aceitação (RN-003)
                if f1 >= self.f1_threshold:
                    modelos_aprovados[key] = {
                        "modelo": model,
                        "f1_score": f1,
                        "features": list(X_train.columns),
                    }
                    logger.info(
                        f"✅ Modelo {key} aprovado! F1: {f1:.4f} >= {self.f1_threshold}"
                    )
                else:
                    logger.info(
                        f"❌ Modelo {key} reprovado. F1: {f1:.4f} < {self.f1_threshold}"
                    )

            except Exception as e:
                logger.error(f"Erro ao treinar modelo {key}: {str(e)}")
                resultado_registro[res_col] = "Erro"

        # 4. Salvar modelos aprovados em arquivo .joblib (RN-003)
        if modelos_aprovados:
            self.salvar_modelos_aprovados(
                modelos_aprovados,
                curso,
                opcao,
                ano,
                periodo,
                tipo_integralizacao,
            )
            resultado_registro["status"] = "OK"
        else:
            logger.warning(
                f"Nenhum modelo treinado para coorte {coorte_str} atingiu o limiar de F1 >= {self.f1_threshold}."
            )
            resultado_registro["status"] = "Sem modelo aceito"

        return resultado_registro

    def salvar_modelos_aprovados(
        self,
        modelos_aprovados: dict,
        curso: str,
        opcao: str,
        ano: int,
        periodo: int,
        tipo_integralizacao: str,
    ):
        """Persiste os modelos aprovados em um arquivo .joblib.

        O arquivo gerado armazena um dicionário com todos os modelos que
        tiveram F1-Score acima do threshold na coorte.

        Args:
            modelos_aprovados: Dicionário contendo modelos e metadados
            curso: Nome do curso
            opcao: Código/turno da opção
            ano: Ano de ingresso da coorte
            periodo: Período de ingresso da coorte
            tipo_integralizacao: String de tipo de integralização
        """
        curso_clean = curso.replace(" ", "_").lower()
        opcao_clean = str(opcao).replace(" ", "_").lower()
        tipo_clean = tipo_integralizacao.lower()

        filename = f"modelos_treinados_{curso_clean}_{opcao_clean}_{ano}_{periodo}_{tipo_clean}.joblib"
        filepath = self.output_dir / filename

        # Preparar dicionário com metadados para salvar
        dados_salvamento = {
            "curso": curso,
            "opcao": opcao,
            "ano_ingresso": ano,
            "periodo_ingresso": periodo,
            "tipo_integralizacao": tipo_integralizacao,
            "modelos": modelos_aprovados,
        }

        joblib.dump(dados_salvamento, filepath)
        logger.info(f"Modelos aprovados da coorte salvos com sucesso em: {filepath}")

    def registrar_resultados(
        self, resultados: list[dict], curso: str, tipo_integralizacao: str
    ):
        """Salva a tabela consolidada de métricas em um arquivo CSV.

        Gera um arquivo de resultados agregados contendo a performance
        de todas as coortes do curso processadas.

        Args:
            resultados: Lista de dicionários de resultados das coortes
            curso: Nome do curso
            tipo_integralizacao: String de tipo de integralização
        """
        if not resultados:
            logger.warning("Lista de resultados vazia. CSV não gerado.")
            return

        df_res = pd.DataFrame(resultados)

        curso_clean = curso.replace(" ", "_").lower()
        tipo_clean = tipo_integralizacao.replace(" ", "_").lower()
        filename = f"modelo_resultado_{curso_clean}_{tipo_clean}.csv"
        filepath = self.resultado_dir / filename

        # Salva em formato CSV com codificação adequada
        df_res.to_csv(filepath, sep=";", index=False, encoding="utf-8")
        logger.info(f"Métricas de treinamento registradas no CSV: {filepath}")
