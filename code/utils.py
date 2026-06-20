import logging
from typing import Any

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("EV_Forecast")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def print_info(message: str) -> None:
    logger = logging.getLogger("EV_Forecast")
    if not logger.handlers:
        logger = setup_logger()
    logger.info(message)

def print_dataframe_info(df: Any, name: str = "DataFrame") -> None:
    print_info(f"--- Info for {name} ---")
    print_info(f"Shape: {df.shape}")
    print_info(f"Missing values: \n{df.isnull().sum()}")
