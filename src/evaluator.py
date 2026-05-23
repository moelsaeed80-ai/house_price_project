"""
Module 5: Evaluator
Detailed model testing, residual analysis, and feature importance.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging

logger = logging.getLogger(__name__)

REPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")


def full_evaluation(model, X_test: pd.DataFrame, y_test: pd.Series, feature_names: list) -> dict:
    """Run all evaluation steps and save plots."""
    y_pred = model.predict(X_test)
    residuals = y_test.values - y_pred

    _plot_actual_vs_predicted(y_test.values, y_pred)
    _plot_residuals(y_pred, residuals)
    _plot_feature_importance(model, feature_names)
    _plot_error_distribution(residuals)

    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    metrics = {
        "MAE": round(mean_absolute_error(y_test, y_pred), 2),
        "RMSE": round(np.sqrt(mean_squared_error(y_test, y_pred)), 2),
        "R2": round(r2_score(y_test, y_pred), 4),
        "MAPE": round(np.mean(np.abs((y_test.values - y_pred) / y_test.values)) * 100, 2),
        "Median_AE": round(float(np.median(np.abs(residuals))), 2),
    }
    logger.info("Evaluation complete. Metrics: %s", metrics)
    return metrics


def _plot_actual_vs_predicted(y_true, y_pred):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(y_true / 1e6, y_pred / 1e6, alpha=0.3, s=8, color='steelblue')
    lim = [min(y_true.min(), y_pred.min()) / 1e6, max(y_true.max(), y_pred.max()) / 1e6]
    ax.plot(lim, lim, 'r--', lw=1.5, label='Perfect prediction')
    ax.set_xlabel('Actual Price (M$)')
    ax.set_ylabel('Predicted Price (M$)')
    ax.set_title('Actual vs Predicted Price')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'actual_vs_predicted.png'), dpi=120)
    plt.close()


def _plot_residuals(y_pred, residuals):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(y_pred / 1e6, residuals / 1e3, alpha=0.3, s=8, color='coral')
    ax.axhline(0, color='black', lw=1)
    ax.set_xlabel('Predicted Price (M$)')
    ax.set_ylabel('Residuals ($K)')
    ax.set_title('Residual Plot')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'residuals.png'), dpi=120)
    plt.close()


def _plot_feature_importance(model, feature_names: list):
    try:
        # Works for Random Forest / GBM
        inner_model = model.named_steps['model']
        if hasattr(inner_model, 'feature_importances_'):
            importances = inner_model.feature_importances_
        else:
            return
        feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=True).tail(15)
        fig, ax = plt.subplots(figsize=(9, 6))
        feat_imp.plot(kind='barh', ax=ax, color='steelblue')
        ax.set_title('Top 15 Feature Importances')
        ax.set_xlabel('Importance')
        plt.tight_layout()
        plt.savefig(os.path.join(REPORTS_DIR, 'feature_importance.png'), dpi=120)
        plt.close()
    except Exception as e:
        logger.warning("Feature importance plot failed: %s", e)


def _plot_error_distribution(residuals):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(residuals / 1e3, bins=80, color='mediumseagreen', edgecolor='white')
    ax.set_xlabel('Error ($K)')
    ax.set_ylabel('Count')
    ax.set_title('Prediction Error Distribution')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'error_distribution.png'), dpi=120)
    plt.close()


def generate_report(metrics: dict, model_name: str) -> str:
    """Generate a plain text report summary."""
    lines = [
        "=" * 50,
        f"  House Price Prediction — Model Evaluation Report",
        f"  Best Model: {model_name}",
        "=" * 50,
        f"  R² Score  : {metrics['R2']}",
        f"  MAE       : ${metrics['MAE']:,.0f}",
        f"  RMSE      : ${metrics['RMSE']:,.0f}",
        f"  MAPE      : {metrics['MAPE']}%",
        f"  Median AE : ${metrics['Median_AE']:,.0f}",
        "=" * 50,
    ]
    report = "\n".join(lines)
    path = os.path.join(REPORTS_DIR, 'model_report.txt')
    with open(path, 'w') as f:
        f.write(report)
    return report


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from data_loader import load_data
    from preprocessor import preprocess, get_feature_columns, get_target_column
    from trainer import split_data, train_all, select_best, save_model

    df = load_data()
    df = preprocess(df)
    features = get_feature_columns()
    target = get_target_column()
    X_train, X_test, y_train, y_test = split_data(df, features, target)
    results = train_all(X_train, X_test, y_train, y_test)
    best_name, best_model, _ = select_best(results)
    metrics = full_evaluation(best_model, X_test, y_test, features)
    print(generate_report(metrics, best_name))
