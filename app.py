"""
Streamlit Web Application — House Price Prediction Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import os
import sys
import joblib

# ── Path setup ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, BASE_DIR)

from src.data_loader import load_data
from src.preprocessor import preprocess, get_feature_columns, get_target_column

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="🏠 House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {background:#f0f4ff;border-radius:10px;padding:16px;text-align:center;}
    .metric-value {font-size:2rem;font-weight:bold;color:#2563eb;}
    .metric-label {font-size:0.85rem;color:#6b7280;}
    .stTabs [data-baseweb="tab"] {font-size:1rem;font-weight:600;}
</style>
""", unsafe_allow_html=True)

# ── Data & model loading ──────────────────────────────────────
@st.cache_data
def get_data():
    df_raw = load_data(os.path.join(BASE_DIR, 'data', 'house_sales.csv'))
    df = preprocess(df_raw)
    return df_raw, df

@st.cache_resource
def get_model():
    path = os.path.join(BASE_DIR, 'models', 'best_model.pkl')
    if os.path.exists(path):
        return joblib.load(path)
    return None

df_raw, df = get_data()
model = get_model()
features = get_feature_columns()
target = get_target_column()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/house.png", width=60)
st.sidebar.title("🏠 House Price Predictor")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Dashboard", "🔍 Data Explorer", "🤖 Model Results", "💰 Price Predictor"],
    label_visibility="collapsed"
)

# ── Page: Dashboard ───────────────────────────────────────────
if page == "📊 Dashboard":
    st.title("📊 House Sales — Dashboard")
    st.markdown("King County, WA · 21,613 sales · 2014–2015")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sales", f"{len(df):,}")
    with col2:
        st.metric("Avg Price", f"${df['price'].mean()/1e6:.2f}M")
    with col3:
        st.metric("Median Price", f"${df['price'].median()/1e3:.0f}K")
    with col4:
        st.metric("Avg Living Area", f"{df['sqft_living'].mean():,.0f} sqft")

    st.markdown("---")
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Price Distribution")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(df['price'] / 1e6, bins=60, color='#3b82f6', edgecolor='white', alpha=0.85)
        ax.set_xlabel("Price (Millions $)", fontsize=11)
        ax.set_ylabel("Count", fontsize=11)
        ax.set_title("Distribution of Sale Prices")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_right:
        st.subheader("Price by Grade")
        fig, ax = plt.subplots(figsize=(7, 4))
        grade_prices = df.groupby('grade')['price'].median() / 1e3
        grade_prices.plot(kind='bar', ax=ax, color='#6366f1', edgecolor='white')
        ax.set_xlabel("Grade", fontsize=11)
        ax.set_ylabel("Median Price ($K)", fontsize=11)
        ax.set_title("Median Price by House Grade")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.subheader("Geographic Price Map")
    map_df = df[['lat', 'long', 'price']].copy()
    map_df.columns = ['lat', 'lon', 'price']
    st.map(map_df.sample(5000, random_state=42), zoom=9)

# ── Page: Data Explorer ───────────────────────────────────────
elif page == "🔍 Data Explorer":
    st.title("🔍 Data Explorer")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📋 Overview", "📈 Feature Plots", "🔗 Correlations"])

    with tab1:
        st.subheader("Raw Dataset (first 100 rows)")
        st.dataframe(df_raw.head(100), use_container_width=True)
        st.subheader("Descriptive Statistics")
        st.dataframe(df_raw.describe().T.round(2), use_container_width=True)

    with tab2:
        st.subheader("Feature vs Price")
        feat_choice = st.selectbox("Select feature", ['sqft_living', 'grade', 'bedrooms', 'bathrooms', 'house_age', 'floors', 'condition'])
        sample = df.sample(min(3000, len(df)), random_state=42)
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.scatter(sample[feat_choice], sample['price'] / 1e6, alpha=0.35, s=8, color='#3b82f6')
        ax.set_xlabel(feat_choice)
        ax.set_ylabel("Price (M$)")
        ax.set_title(f"Price vs {feat_choice}")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with tab3:
        st.subheader("Top Correlations with Price")
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        corr = df[num_cols].corr()['price'].drop('price').sort_values(ascending=False)
        top = corr.head(12)
        fig, ax = plt.subplots(figsize=(9, 5))
        colors = ['#22c55e' if v > 0 else '#ef4444' for v in top.values]
        top.plot(kind='bar', ax=ax, color=colors, edgecolor='white')
        ax.set_title("Feature Correlations with Price")
        ax.set_ylabel("Pearson r")
        ax.axhline(0, color='black', lw=0.8)
        plt.xticks(rotation=35, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# ── Page: Model Results ───────────────────────────────────────
elif page == "🤖 Model Results":
    st.title("🤖 Model Results")
    st.markdown("---")

    report_path = os.path.join(BASE_DIR, 'reports', 'model_report.txt')
    if os.path.exists(report_path):
        with open(report_path) as f:
            st.code(f.read(), language=None)

    st.subheader("Model Comparison")
    comparison = pd.DataFrame({
        "Model": ["Ridge Regression", "Random Forest", "Gradient Boosting"],
        "R²": [0.7034, 0.8595, 0.8889],
        "MAE ($)": [126321, 73041, 68984],
        "RMSE ($)": [207042, 142487, 126683],
        "MAPE (%)": ["~18%", "~13%", "~12.8%"],
    }).set_index("Model")
    st.dataframe(comparison, use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    comparison['R²'].plot(kind='bar', ax=ax, color=['#94a3b8', '#60a5fa', '#22c55e'], edgecolor='white')
    ax.set_title("R² Score by Model")
    ax.set_ylabel("R²")
    ax.set_ylim(0, 1)
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.subheader("Evaluation Plots")
    col1, col2 = st.columns(2)
    plots = {
        "Actual vs Predicted": "actual_vs_predicted.png",
        "Residuals": "residuals.png",
        "Feature Importance": "feature_importance.png",
        "Error Distribution": "error_distribution.png",
    }
    cols = [col1, col2, col1, col2]
    for (title, fname), col in zip(plots.items(), cols):
        img_path = os.path.join(BASE_DIR, 'reports', fname)
        if os.path.exists(img_path):
            with col:
                st.subheader(title)
                st.image(img_path, use_container_width=True)

# ── Page: Price Predictor ─────────────────────────────────────
elif page == "💰 Price Predictor":
    st.title("💰 Predict House Price")
    st.markdown("Adjust the sliders to get an instant price prediction.")
    st.markdown("---")

    if model is None:
        st.warning("⚠️ Model not found. Please run `python main.py` first.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🏗️ Size & Structure")
            sqft_living = st.slider("Living Area (sqft)", 300, 10000, 2000, step=50)
            sqft_lot = st.slider("Lot Size (sqft)", 500, 100000, 7500, step=500)
            sqft_above = st.slider("Above Ground (sqft)", 300, 8000, 1800, step=50)
            sqft_basement = st.slider("Basement (sqft)", 0, 3000, 0, step=50)
            floors = st.selectbox("Floors", [1.0, 1.5, 2.0, 2.5, 3.0])

        with col2:
            st.subheader("🛏️ Rooms & Quality")
            bedrooms = st.slider("Bedrooms", 0, 10, 3)
            bathrooms = st.slider("Bathrooms", 0.0, 6.0, 2.0, step=0.25)
            grade = st.slider("Grade (1–13)", 1, 13, 7)
            condition = st.slider("Condition (1–5)", 1, 5, 3)
            waterfront = st.checkbox("Waterfront")
            view = st.slider("View Score (0–4)", 0, 4, 0)

        with col3:
            st.subheader("📍 Location & Age")
            lat = st.slider("Latitude", 47.15, 47.78, 47.55, step=0.01)
            long_ = st.slider("Longitude", -122.52, -121.31, -122.2, step=0.01)
            yr_built = st.slider("Year Built", 1900, 2015, 1990)
            sqft_living15 = st.slider("Neighbors' Avg Sqft", 400, 6000, 1985, step=50)
            sqft_lot15 = st.slider("Neighbors' Lot Avg", 500, 50000, 8000, step=500)
            was_renovated = st.checkbox("Was Renovated")

        # Build input
        sale_year = 2015
        sale_month = 5
        house_age = sale_year - yr_built
        renovated_age = house_age if not was_renovated else house_age // 2
        total_rooms = bedrooms + bathrooms
        basement_flag = int(sqft_basement > 0)

        input_dict = {
            'bedrooms': bedrooms, 'bathrooms': bathrooms,
            'sqft_living': sqft_living, 'sqft_lot': sqft_lot,
            'floors': floors, 'waterfront': int(waterfront), 'view': view,
            'condition': condition, 'grade': grade,
            'sqft_above': sqft_above, 'sqft_basement': sqft_basement,
            'yr_built': yr_built, 'lat': lat, 'long': long_,
            'sqft_living15': sqft_living15, 'sqft_lot15': sqft_lot15,
            'sale_year': sale_year, 'sale_month': sale_month,
            'house_age': house_age, 'was_renovated': int(was_renovated),
            'renovated_age': renovated_age,
            'total_rooms': total_rooms, 'basement_flag': basement_flag,
        }

        input_df = pd.DataFrame([input_dict])[features]

        st.markdown("---")
        if st.button("🔮 Predict Price", type="primary", use_container_width=True):
            prediction = model.predict(input_df)[0]
            low = prediction * 0.88
            high = prediction * 1.12

            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Low Estimate", f"${low:,.0f}")
            with col_b:
                st.metric("🏠 Predicted Price", f"${prediction:,.0f}", delta=None)
            with col_c:
                st.metric("High Estimate", f"${high:,.0f}")

            # Price range bar
            fig, ax = plt.subplots(figsize=(8, 1.5))
            ax.barh(0, high - low, left=low, color='#3b82f6', alpha=0.3, height=0.4)
            ax.plot([prediction], [0], 'r|', markersize=20, markeredgewidth=3, label=f'${prediction:,.0f}')
            ax.set_xlabel("Price ($)")
            ax.set_yticks([])
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))
            ax.legend(loc='upper right')
            ax.set_title("Prediction Confidence Range (±12%)")
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
