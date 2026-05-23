# 🏠 House Price Prediction — Final Project

## Project Structure (Modular)

```
house_price_project/
├── data/
│   └── house_sales.csv          # King County, WA — 21,613 records
├── src/
│   ├── data_loader.py           # Module 1: Load & validate data
│   ├── preprocessor.py          # Module 2: Clean & feature engineering
│   ├── analyzer.py              # Module 3: EDA & plots
│   ├── trainer.py               # Module 4: Train & save models
│   └── evaluator.py             # Module 5: Evaluate & report
├── models/
│   └── best_model.pkl           # Saved Gradient Boosting model
├── reports/
│   ├── price_distribution.png
│   ├── correlation_heatmap.png
│   ├── price_vs_features.png
│   ├── geo_price_map.png
│   ├── actual_vs_predicted.png
│   ├── residuals.png
│   ├── feature_importance.png
│   ├── error_distribution.png
│   └── model_report.txt
├── tests/
│   └── test_pipeline.py         # 11 unit tests
├── main.py                      # Full pipeline runner
├── app.py                       # Streamlit web app
└── README.md
```

## Quickstart

```bash
# 1. Install dependencies
pip install pandas scikit-learn joblib matplotlib seaborn streamlit

# 2. Run full pipeline (train + evaluate + save plots)
python main.py

# 3. Run tests
pytest tests/test_pipeline.py -v

# 4. Launch Streamlit app
streamlit run app.py
```

## Results Summary

| Model              | R²     | MAE      | RMSE     |
|--------------------|--------|----------|----------|
| Ridge Regression   | 0.703  | $126,321 | $207,042 |
| Random Forest      | 0.860  | $73,041  | $142,487 |
| **Gradient Boosting** | **0.889** | **$68,984** | **$126,683** |

## Streamlit App Pages

1. **📊 Dashboard** — KPIs, price distribution, price-by-grade chart, geographic map
2. **🔍 Data Explorer** — Raw data, statistics, feature vs price scatter, correlations
3. **🤖 Model Results** — Model comparison, evaluation plots, feature importance
4. **💰 Price Predictor** — Live prediction with 30+ input sliders & confidence range
