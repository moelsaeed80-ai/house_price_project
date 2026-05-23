"""
Main Pipeline Runner
Orchestrates: load → preprocess → analyze → train → evaluate
"""

import sys
import os
import logging

sys.path.insert(0, os.path.dirname(__file__))

from src.data_loader import load_data, get_data_info
from src.preprocessor import preprocess, get_feature_columns, get_target_column
from src.analyzer import run_eda
from src.trainer import split_data, train_all, select_best, save_model
from src.evaluator import full_evaluation, generate_report

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s] %(message)s')
logger = logging.getLogger("pipeline")


def run_pipeline(data_path: str = None):
    logger.info("=" * 55)
    logger.info("  House Price Prediction — Full Pipeline")
    logger.info("=" * 55)

    # Step 1: Load
    logger.info("STEP 1: Loading data...")
    df_raw = load_data(data_path) if data_path else load_data()
    info = get_data_info(df_raw)
    logger.info(f"  Rows: {info['rows']}, Columns: {info['columns']}")

    # Step 2: Preprocess
    logger.info("STEP 2: Preprocessing...")
    df = preprocess(df_raw)
    features = get_feature_columns()
    target = get_target_column()

    # Step 3: EDA
    logger.info("STEP 3: Exploratory Data Analysis...")
    stats = run_eda(df)
    logger.info(f"  EDA stats: {stats['basic']}")

    # Step 4: Train
    logger.info("STEP 4: Training models...")
    X_train, X_test, y_train, y_test = split_data(df, features, target)
    all_results = train_all(X_train, X_test, y_train, y_test)
    best_name, best_model, train_metrics = select_best(all_results)
    model_path = save_model(best_model)

    # Step 5: Evaluate
    logger.info("STEP 5: Evaluating best model...")
    eval_metrics = full_evaluation(best_model, X_test, y_test, features)
    report = generate_report(eval_metrics, best_name)
    print("\n" + report)

    # Summary for Streamlit
    all_metrics = {k: v['metrics'] for k, v in all_results.items()}

    logger.info("Pipeline complete! All outputs in reports/ and models/")
    return {
        "best_model_name": best_name,
        "best_model_path": model_path,
        "eval_metrics": eval_metrics,
        "all_metrics": all_metrics,
        "eda_stats": stats['basic'],
        "feature_names": features,
    }


if __name__ == "__main__":
    run_pipeline()
