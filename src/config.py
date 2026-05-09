"""Configuração de logging para o projeto Magra."""

import logging
import sys
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent.parent / "output" / "logs"


def setup_logging(level: str = "DEBUG") -> logging.Logger:
    """Configura logging centralizado para o projeto.

    Args:
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Logger configurado
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = OUTPUT_DIR / f"magra_{timestamp}.log"

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )

    logger = logging.getLogger("magra")
    logger.info(f"Logging iniciado. Arquivo: {log_file}")

    return logger


def get_logger(name: str = "magra") -> logging.Logger:
    """Retorna logger configurado.

    Args:
        name: Nome do logger

    Returns:
        Logger instance
    """
    return logging.getLogger(name)