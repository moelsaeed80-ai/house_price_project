"""
Module 6: Tests
Unit tests for each module.
"""

import sys
import os
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import load_data, get_data_info
from src.preprocessor import preprocess, get_feature_columns, get_target_column, _engineer_features, _remove_outliers
from src.trainer import build_models, evaluate_model, split_data

# ─── Fixtures ────────────────────────────────────────────────

@pytest.fixture(scope="module")
def raw_df():
    return load_data()

@pytest.fixture(scope="module")
def clean_df(raw_df):
    return preprocess(raw_df)

# ─── Data Loader Tests ───────────────────────────────────────

def test_load_data_shape(raw_df):
    assert raw_df.shape[0] > 1000, "Dataset should have more than 1000 rows"
    assert raw_df.shape[1] == 20, "Expected 20 columns"

def test_load_data_columns(raw_df):
    expected = ['price', 'bedrooms', 'bathrooms', 'sqft_living', 'grade']
    for col in expected:
        assert col in raw_df.columns, f"Missing column: {col}"

def test_data_info(raw_df):
    info = get_data_info(raw_df)
    assert info['rows'] > 0
    assert info['columns'] > 0
    assert isinstance(info['missing_values'], dict)

# ─── Preprocessor Tests ──────────────────────────────────────

def test_preprocess_output_columns(clean_df):
    for col in get_feature_columns():
        assert col in clean_df.columns, f"Missing engineered column: {col}"

def test_remove_outliers():
    df = pd.DataFrame({'bedrooms': [3, 33, 5], 'price': [300000, 999999, 450000]})
    result = _remove_outliers(df)
    assert len(result) == 2, "Should remove the 33-bedroom row"
    assert (result['bedrooms'] <= 10).all()

def test_engineer_features():
    df = pd.DataFrame({
        'price': [500000],
        'sqft_living': [2000],
        'bedrooms': [3],
        'bathrooms': [2.0],
        'sqft_basement': [500],
        'yr_built': [1990],
        'yr_renovated': [2005],
        'sale_year': [2014],
    })
    result = _engineer_features(df)
    assert 'house_age' in result.columns
    assert 'was_renovated' in result.columns
    assert result['was_renovated'].iloc[0] == 1
    assert result['house_age'].iloc[0] == 24
    assert result['price_per_sqft'].iloc[0] == 250.0

def test_no_missing_values_in_features(clean_df):
    for col in get_feature_columns():
        missing = clean_df[col].isnull().sum()
        assert missing == 0, f"Feature {col} has {missing} missing values"

def test_target_column_positive(clean_df):
    assert (clean_df[get_target_column()] > 0).all(), "All prices must be positive"

# ─── Trainer Tests ───────────────────────────────────────────

def test_build_models_keys():
    models = build_models()
    assert "Ridge Regression" in models
    assert "Random Forest" in models
    assert "Gradient Boosting" in models

def test_split_data(clean_df):
    features = get_feature_columns()
    target = get_target_column()
    X_train, X_test, y_train, y_test = split_data(clean_df, features, target)
    total = len(X_train) + len(X_test)
    assert abs(total - len(clean_df)) <= 1
    assert len(X_test) / total == pytest.approx(0.2, abs=0.01)

def test_evaluate_model(clean_df):
    features = get_feature_columns()
    target = get_target_column()
    X_train, X_test, y_train, y_test = split_data(clean_df, features, target)
    from sklearn.dummy import DummyRegressor
    from sklearn.pipeline import Pipeline
    dummy = Pipeline([('model', DummyRegressor(strategy='mean'))])
    dummy.fit(X_train, y_train)
    metrics = evaluate_model(dummy, X_test, y_test)
    assert 'MAE' in metrics
    assert 'R2' in metrics
    assert 'RMSE' in metrics
    assert metrics['R2'] <= 1.0

# ─── Run ─────────────────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
