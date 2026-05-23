"""
Module 3: Analyzer
Exploratory Data Analysis — generates statistics and saves plots.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import os
import logging

logger = logging.getLogger(__name__)

REPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")


def run_eda(df: pd.DataFrame) -> dict:
    """Run full EDA and return summary statistics dict."""
    stats = {}
    stats['basic'] = _basic_stats(df)
    _plot_price_distribution(df)
    _plot_correlation_heatmap(df)
    _plot_price_vs_features(df)
    _plot_geo_scatter(df)
    logger.info("EDA complete. Plots saved to reports/")
    return stats


def _basic_stats(df: pd.DataFrame) -> dict:
    price = df['price']
    return {
        "count": int(len(df)),
        "mean_price": round(float(price.mean()), 2),
        "median_price": round(float(price.median()), 2),
        "min_price": round(float(price.min()), 2),
        "max_price": round(float(price.max()), 2),
        "std_price": round(float(price.std()), 2),
        "avg_sqft": round(float(df['sqft_living'].mean()), 2),
        "avg_bedrooms": round(float(df['bedrooms'].mean()), 2),
        "waterfront_pct": round(float(df['waterfront'].mean() * 100), 2),
    }


def _plot_price_distribution(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(df['price'] / 1e6, bins=60, color='steelblue', edgecolor='white')
    axes[0].set_title('Price Distribution')
    axes[0].set_xlabel('Price (Millions $)')
    axes[0].set_ylabel('Count')

    axes[1].hist(np.log1p(df['price']), bins=60, color='coral', edgecolor='white')
    axes[1].set_title('Log-Price Distribution')
    axes[1].set_xlabel('log(Price)')
    axes[1].set_ylabel('Count')

    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'price_distribution.png'), dpi=120)
    plt.close()


def _plot_correlation_heatmap(df: pd.DataFrame):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(16, 12))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                linewidths=0.5, ax=ax, annot_kws={"size": 7})
    ax.set_title('Feature Correlation Heatmap', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'correlation_heatmap.png'), dpi=120)
    plt.close()


def _plot_price_vs_features(df: pd.DataFrame):
    features = ['sqft_living', 'grade', 'bedrooms', 'house_age']
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    for i, feat in enumerate(features):
        if feat not in df.columns:
            continue
        axes[i].scatter(df[feat], df['price'] / 1e6, alpha=0.3, s=8, color='steelblue')
        axes[i].set_xlabel(feat)
        axes[i].set_ylabel('Price (M$)')
        axes[i].set_title(f'Price vs {feat}')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'price_vs_features.png'), dpi=120)
    plt.close()


def _plot_geo_scatter(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 8))
    sc = ax.scatter(df['long'], df['lat'], c=df['price'] / 1e6,
                    cmap='plasma', alpha=0.4, s=6)
    plt.colorbar(sc, ax=ax, label='Price (M$)')
    ax.set_title('Geographic Price Distribution')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'geo_price_map.png'), dpi=120)
    plt.close()


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from data_loader import load_data
    from preprocessor import preprocess
    df = load_data()
    df = preprocess(df)
    stats = run_eda(df)
    print("EDA Stats:", stats)
