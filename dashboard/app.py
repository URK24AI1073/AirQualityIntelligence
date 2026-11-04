
from pathlib import Path
import json

import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "processed" / "air_quality_cleaned.csv"
MODEL_FILE = ROOT / "models" / "xgboost.joblib"
METRICS_FILE = ROOT / "reports" / "xgboost_metrics.json"

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Air Quality Intelligence",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Cloud-Based Air Quality Intelligence")
st.caption(
    "Cloud-Native Spatiotemporal Air Quality Forecasting "
    "and Environmental Intelligence"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        return None

    df = pd.read_csv(DATA_FILE)

    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(
            df["Timestamp"], errors="coerce"
        )

    return df


@st.cache_resource
def load_model():
    if not MODEL_FILE.exists():
        return None

    return joblib.load(MODEL_FILE)


@st.cache_data
def load_metrics():
    if not METRICS_FILE.exists():
        return {}

    with open(METRICS_FILE, "r") as file:
        return json.load(file)


df = load_data()
model = load_model()
model_metrics = load_metrics()

if df is None:
    st.error("Processed dataset not found.")
    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a section",
    [
        "Dashboard",
        "Prediction",
        "Model Performance",
        "Dataset",
        "CI/CD Pipeline"
    ]
)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.header("Air Quality Overview")

    total_records = len(df)

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    available_measurements = len(numeric_columns)

    missing_values = int(df.isnull().sum().sum())

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", f"{total_records:,}")
    col2.metric("Available Measurements", available_measurements)
    col3.metric("Missing Values", f"{missing_values:,}")

    st.divider()

    st.subheader("Pollutant Analysis")

    pollutants = [
        col for col in ["CO(GT)", "NO2(GT)", "C6H6(GT)"]
        if col in df.columns
    ]

    if pollutants:
        selected_pollutant = st.selectbox(
            "Select pollutant",
            pollutants
        )

        chart_data = df[selected_pollutant].dropna()

        if not chart_data.empty:
            fig = px.histogram(
                x=chart_data,
                nbins=40,
                title=f"Distribution of {selected_pollutant}",
                labels={"x": selected_pollutant}
            )

            st.plotly_chart(fig, use_container_width=True)

        if "Timestamp" in df.columns:
            trend_data = df[
                ["Timestamp", selected_pollutant]
            ].dropna()

            if not trend_data.empty:
                trend_fig = px.line(
                    trend_data,
                    x="Timestamp",
                    y=selected_pollutant,
                    title=f"{selected_pollutant} Over Time"
                )

                st.plotly_chart(
                    trend_fig,
                    use_container_width=True
                )
    else:
        st.warning("Pollutant columns are unavailable.")

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

elif page == "Prediction":

    st.header("Air Quality Prediction")
    st.write("Enter sensor measurements to predict CO(GT).")

    features = [
        "PT08.S1(CO)",
        "PT08.S2(NMHC)",
        "PT08.S3(NOx)",
        "PT08.S4(NO2)",
        "PT08.S5(O3)",
        "T",
        "RH",
        "AH"
    ]

    if model is None:
        st.error("XGBoost model file not found.")
    else:
        with st.form("prediction_form"):

            values = {}

            col1, col2 = st.columns(2)

            for index, feature in enumerate(features):
                with col1 if index % 2 == 0 else col2:
                    default_value = 0.0

                    if feature in df.columns:
                        valid_values = pd.to_numeric(
                            df[feature], errors="coerce"
                        ).dropna()

                        if not valid_values.empty:
                            default_value = float(
                                valid_values.median()
                            )

                    values[feature] = st.number_input(
                        feature,
                        value=default_value,
                        format="%.4f"
                    )

            submitted = st.form_submit_button(
                "Predict Air Quality"
            )

        if submitted:
            input_df = pd.DataFrame(
                [values],
                columns=features
            )

            try:
                prediction = model.predict(input_df)

                st.success(
                    f"Predicted CO(GT): {prediction[0]:.4f}"
                )

            except Exception as error:
                st.error(f"Prediction failed: {error}")

# --------------------------------------------------
# MODEL PERFORMANCE
# --------------------------------------------------

elif page == "Model Performance":

    st.header("XGBoost Model Performance")

    if model_metrics:
        col1, col2, col3 = st.columns(3)

        mae = model_metrics.get("MAE")
        rmse = model_metrics.get("RMSE")
        r2 = model_metrics.get("R2")

        if mae is not None:
            col1.metric("MAE", f"{float(mae):.4f}")

        if rmse is not None:
            col2.metric("RMSE", f"{float(rmse):.4f}")

        if r2 is not None:
            col3.metric("R² Score", f"{float(r2):.4f}")

        st.info(
            "These values are loaded from the saved model "
            "evaluation report."
        )
    else:
        st.warning("Model metrics file not found.")

# --------------------------------------------------
# DATASET
# --------------------------------------------------

elif page == "Dataset":

    st.header("Cleaned Air Quality Dataset")

    st.write("Dataset shape:", df.shape)

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    st.subheader("Missing Values by Column")

    missing = df.isnull().sum().reset_index()
    missing.columns = ["Column", "Missing Values"]

    st.dataframe(
        missing,
        use_container_width=True
    )

# --------------------------------------------------
# CI/CD PIPELINE
# --------------------------------------------------

elif page == "CI/CD Pipeline":

    st.header("Cloud CI/CD Pipeline")

    st.write(
        "Continuous Integration and Continuous Deployment "
        "for the Air Quality Intelligence project."
    )

    st.subheader("Pipeline Status")

    col1, col2 = st.columns(2)

    with col1:
        st.success("ETL Pipeline: Previously verified")
        st.success("GitHub Actions CI: Previously passed")

    with col2:
        st.success("Docker Deployment: Previously verified")
        st.success("Render Hosting: Previously verified")

    st.caption(
        "These are recorded project statuses, not live checks. "
        "Use the links below to verify the latest workflow and deployment."
    )

    st.divider()

    st.subheader("GitHub Actions")

    st.write(
        "The GitHub Actions workflow runs the ETL pipeline "
        "and checks whether the processed dataset is generated."
    )

    st.link_button(
        "View GitHub Actions",
        "https://github.com/URK24AI1073/AirQualityIntelligence/actions"
    )

    st.divider()

    st.subheader("Cloud Deployment")

    st.write(
        "Render hosts the public Air Quality Intelligence dashboard "
        "and deploys changes from the connected GitHub repository."
    )

    st.link_button(
        "Open Live Dashboard",
        "https://airqualityintelligence.onrender.com"
    )

    st.link_button(
        "View GitHub Repository",
        "https://github.com/URK24AI1073/AirQualityIntelligence"
    )

    st.divider()

    st.subheader("Project Architecture")

    st.code(
        """
        AirQualityUCI.csv
                |
                v
          Data Cleaning
                |
                v
             ETL
                |
                v
        Processed Dataset
                |
                v
          XGBoost Model
                |
                v
        Streamlit Dashboard
                |
                v
          Docker Image
                |
                v
          Render Cloud

        GitHub Push
             |
             v
        GitHub Actions CI
             |
             v
        Render Auto Deployment
        """,
        language="text"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Air Quality Intelligence | Cloud Computing for Data Analytics"
)

