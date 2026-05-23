"""
Module 1: Data Loader
Handles downloading and loading of house sales data.
"""

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'house_sales.csv')


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Load raw house sales data from CSV."""
    logger.info(f"Loading data from {path}")
    df = pd.read_csv(path)
    logger.info(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
    return df


def get_data_info(df: pd.DataFrame) -> dict:
    """Return basic metadata about the dataset."""
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1e6, 2),
    }


if __name__ == "__main__":
    df = load_data()
    info = get_data_info(df)
    print("Dataset Info:")
    for k, v in info.items():
        print(f"  {k}: {v}")
