
from pathlib import Path
import json

import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "processed" / "air_quality_cleaned.csv"
MODEL_FILE = ROOT / "models" / "xgboost.joblib"
METRICS_FILE = ROOT / "reports" / "xgboost_metrics.json"

FEATURES = [
    "PT08.S1(CO)",
    "PT08.S2(NMHC)",
    "PT08.S3(NOx)",
    "PT08.S4(NO2)",
    "PT08.S5(O3)",
    "T",
    "RH",
    "AH",
]

st.set_page_config(
    page_title="Air Quality Intelligence",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Cloud-Based Air Quality Intelligence")
st.caption(
    "Air-quality analytics, machine learning predictions, "
    "and environmental data visualization"
)

if not DATA_FILE.exists():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()

if not MODEL_FILE.exists():
    st.error(f"Trained model not found: {MODEL_FILE}")
    st.stop()

df = pd.read_csv(DATA_FILE)
model = joblib.load(MODEL_FILE)

# Convert available measurements to numeric values
for col in df.columns:
    if col not in ["Date", "Time", "Timestamp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Sidebar
st.sidebar.header("Dashboard Controls")

numeric_columns = df.select_dtypes(include="number").columns.tolist()
available_targets = [
    col for col in ["CO(GT)", "NO2(GT)", "C6H6(GT)"]
    if col in numeric_columns and df[col].notna().any()
]

selected_target = st.sidebar.selectbox(
    "Pollutant to visualize",
    available_targets if available_targets else numeric_columns,
)

# Summary metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", f"{len(df):,}")
col2.metric("Available Measurements", len(numeric_columns))
col3.metric(
    "Missing Values",
    f"{int(df[numeric_columns].isna().sum().sum()):,}"
)

st.divider()

# Data visualization
st.subheader(f"{selected_target} — Distribution")

valid_values = df[selected_target].dropna()

if not valid_values.empty:
    fig = px.histogram(
        df,
        x=selected_target,
        nbins=40,
        title=f"Distribution of {selected_target}",
        template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)

# Time series
if "Timestamp" in df.columns:
    time_df = df[["Timestamp", selected_target]].copy()
    time_df["Timestamp"] = pd.to_datetime(
        time_df["Timestamp"], errors="coerce"
    )
    time_df = time_df.dropna().sort_values("Timestamp")

    if not time_df.empty:
        st.subheader("Pollution Trends Over Time")
        trend = px.line(
            time_df,
            x="Timestamp",
            y=selected_target,
            title=f"{selected_target} over time",
            template="plotly_white",
        )
        st.plotly_chart(trend, use_container_width=True)

# Prediction
st.divider()
st.subheader("🤖 CO Pollution Prediction")
st.write(
    "Enter sensor measurements and environmental conditions "
    "to estimate CO(GT) using the trained XGBoost model."
)

if all(feature in df.columns for feature in FEATURES):
    defaults = {}

    for feature in FEATURES:
        median_value = df[feature].median()
        defaults[feature] = (
            float(median_value) if pd.notna(median_value) else 0.0
        )

    with st.form("prediction_form"):
        inputs = {}
        input_columns = st.columns(2)

        for i, feature in enumerate(FEATURES):
            with input_columns[i % 2]:
                inputs[feature] = st.number_input(
                    feature,
                    value=defaults[feature],
                    format="%.3f",
                )

        submitted = st.form_submit_button("Predict CO Level")

    if submitted:
        input_df = pd.DataFrame([inputs], columns=FEATURES)
        prediction = float(model.predict(input_df)[0])

        st.success(f"Estimated CO(GT): {prediction:.3f} mg/m³")
        st.caption(
            "This is a model estimate, not an official air-quality "
            "measurement or health-safety determination."
        )
else:
    st.warning(
        "Prediction is unavailable because one or more required "
        "sensor features are missing from the cleaned dataset."
    )

# Model performance
if METRICS_FILE.exists():
    with open(METRICS_FILE, "r") as file:
        metrics = json.load(file)

    st.divider()
    st.subheader("📊 XGBoost Model Performance")

    m1, m2, m3 = st.columns(3)
    m1.metric("MAE", f"{metrics['MAE']:.4f}")
    m2.metric("RMSE", f"{metrics['RMSE']:.4f}")
    m3.metric("R² Score", f"{metrics['R2']:.4f}")

# Preview
with st.expander("View cleaned dataset"):
    st.dataframe(df.head(100), use_container_width=True)

st.caption("Academic prototype | Air Quality Intelligence")
