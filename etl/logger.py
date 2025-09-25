import logging
from pathlib import Path

# Skapar sökväg för loggfiler (säkerställ att mappen finns)
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

info_log_path = log_dir / "etl_log.txt"
error_log_path = log_dir / "etl_error_log.txt"

def _setup_logger(name: str, path: Path, level: int, fmt: str):
    logger = logging.getLogger(name)
    # Förhindrar att loggar "bubblar upp" och skrivs flera gånger
    logger.propagate = False
    if not logger.handlers:
        handler = logging.FileHandler(path, mode="a", encoding="utf-8")
        formatter = logging.Formatter(fmt, "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

info_logger = _setup_logger("etl_info", info_log_path, logging.INFO, "%(asctime)s - INFO - %(message)s")
error_logger = _setup_logger("etl_error", error_log_path, logging.ERROR, "%(asctime)s - ERROR - %(message)s")

def log_info(message: str):
    info_logger.info(message)

def log_error(message: str):
    error_logger.error(message)
