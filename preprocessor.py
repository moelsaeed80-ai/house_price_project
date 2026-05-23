"""
Module 2: Preprocessor
Cleans and engineers features from raw house sales data.
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Full preprocessing pipeline."""
    df = df.copy()
    df = _parse_dates(df)
    df = _remove_outliers(df)
    df = _engineer_features(df)
    df = _drop_unnecessary(df)
    logger.info(f"Preprocessing complete. Shape: {df.shape}")
    return df


def _parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Parse date column and extract year/month."""
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%dT%H%M%S', errors='coerce')
    df['sale_year'] = df['date'].dt.year
    df['sale_month'] = df['date'].dt.month
    return df


def _remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Remove extreme outliers (e.g., 33 bedrooms)."""
    before = len(df)
    df = df[df['bedrooms'] <= 10]
    df = df[df['price'] > 0]
    logger.info(f"Removed {before - len(df)} outlier rows.")
    return df


def _engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create new useful features."""
    df['house_age'] = df['sale_year'] - df['yr_built']
    df['was_renovated'] = (df['yr_renovated'] > 0).astype(int)
    df['renovated_age'] = df.apply(
        lambda r: r['sale_year'] - r['yr_renovated'] if r['yr_renovated'] > 0 else r['house_age'], axis=1
    )
    df['price_per_sqft'] = df['price'] / df['sqft_living']
    df['total_rooms'] = df['bedrooms'] + df['bathrooms']
    df['basement_flag'] = (df['sqft_basement'] > 0).astype(int)
    df['log_price'] = np.log1p(df['price'])
    return df


def _drop_unnecessary(df: pd.DataFrame) -> pd.DataFrame:
    """Drop columns not used in modelling."""
    drop_cols = ['date', 'yr_renovated', 'zipcode']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return df


def get_feature_columns() -> list:
    """Return the feature columns used for modelling."""
    return [
        'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
        'waterfront', 'view', 'condition', 'grade', 'sqft_above',
        'sqft_basement', 'yr_built', 'lat', 'long', 'sqft_living15',
        'sqft_lot15', 'sale_year', 'sale_month', 'house_age',
        'was_renovated', 'renovated_age', 'total_rooms', 'basement_flag'
    ]


def get_target_column() -> str:
    return 'price'


if __name__ == "__main__":
    from data_loader import load_data
    df = load_data()
    df_clean = preprocess(df)
    print(df_clean[get_feature_columns() + [get_target_column()]].head())
    print("Features:", get_feature_columns())
