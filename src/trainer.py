"""
Module 4: Trainer
Trains multiple regression models and selects the best one.
"""

import pandas as pd
import numpy as np
import os
import joblib
import logging
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
os.makedirs(MODELS_DIR, exist_ok=True)


def split_data(df: pd.DataFrame, features: list, target: str, test_size: float = 0.2, random_state: int = 42):
    """Split dataset into train/test sets."""
    X = df[features]
    y = df[target]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def build_models() -> dict:
    """Return dict of candidate model pipelines."""
    return {
        "Ridge Regression": Pipeline([
            ('scaler', StandardScaler()),
            ('model', Ridge(alpha=10.0))
        ]),
        "Random Forest": Pipeline([
            ('scaler', StandardScaler()),
            ('model', RandomForestRegressor(n_estimators=150, max_depth=15,
                                            random_state=42, n_jobs=-1))
        ]),
        "Gradient Boosting": Pipeline([
            ('scaler', StandardScaler()),
            ('model', GradientBoostingRegressor(n_estimators=200, max_depth=5,
                                                learning_rate=0.1, random_state=42))
        ]),
    }


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Return evaluation metrics for a trained model."""
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    return {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 4),
        "MAPE": round(mape, 2),
    }


def train_all(X_train, X_test, y_train, y_test) -> dict:
    """Train all candidate models and return results."""
    models = build_models()
    results = {}

    for name, pipeline in models.items():
        logger.info(f"Training {name}...")
        pipeline.fit(X_train, y_train)
        metrics = evaluate_model(pipeline, X_test, y_test)
        results[name] = {"pipeline": pipeline, "metrics": metrics}
        logger.info(f"  {name} → R²={metrics['R2']}, RMSE=${metrics['RMSE']:,.0f}, MAE=${metrics['MAE']:,.0f}")

    return results


def select_best(results: dict) -> tuple:
    """Select model with best R² score."""
    best_name = max(results, key=lambda k: results[k]['metrics']['R2'])
    best = results[best_name]
    logger.info(f"Best model: {best_name} (R²={best['metrics']['R2']})")
    return best_name, best['pipeline'], best['metrics']


def save_model(model, name: str = "best_model"):
    """Persist the best model to disk."""
    path = os.path.join(MODELS_DIR, f"{name}.pkl")
    joblib.dump(model, path)
    logger.info(f"Model saved to {path}")
    return path


def load_model(name: str = "best_model"):
    """Load a saved model from disk."""
    path = os.path.join(MODELS_DIR, f"{name}.pkl")
    model = joblib.load(path)
    logger.info(f"Model loaded from {path}")
    return model


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from data_loader import load_data
    from preprocessor import preprocess, get_feature_columns, get_target_column

    df = load_data()
    df = preprocess(df)
    features = get_feature_columns()
    target = get_target_column()

    X_train, X_test, y_train, y_test = split_data(df, features, target)
    results = train_all(X_train, X_test, y_train, y_test)
    best_name, best_model, best_metrics = select_best(results)
    save_model(best_model)
    print(f"\nBest: {best_name}")
    print("Metrics:", best_metrics)
