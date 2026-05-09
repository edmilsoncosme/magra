from src.config import setup_logging

logger = setup_logging("DEBUG")

logger.debug("Mensagem DEBUG")
logger.info("Mensagem INFO")
logger.warning("Mensagem WARNING")
logger.error("Mensagem ERROR")

print("\nLogger configurado com sucesso!")