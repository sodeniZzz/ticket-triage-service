import logging
import logging.config
from pathlib import Path

from src.scripts.io_utils import ROOT_PATH, read_json


def setup_logging(log_config=None, default_level=logging.INFO):
    """
    Setup logging configuration from JSON file.
    """
    if log_config is None:
        log_config = ROOT_PATH / "src" / "logger" / "logger_config.json"
    log_config = Path(log_config)

    if log_config.is_file():
        config = read_json(log_config)
        logging.config.dictConfig(config)
    else:
        print(f"[logger] Config not found at {log_config}, using basicConfig")
        logging.basicConfig(level=default_level)
