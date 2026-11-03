"http://localhost:3000",
"http://127.0.0.1:3000",
from pathlib import Path
import json

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

MODEL_PATH = PROJECT_DIR / "models" / "xgboost.joblib"
METRICS_PATH = PROJECT_DIR / "reports" / "xgboost_metrics.json"


# --------------------------------------------------
# 2. MODEL FEATURES
# Must match train_xgboost.py exactly
# --------------------------------------------------

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


# --------------------------------------------------
# 3. FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Air Quality Intelligence ML API",
    description="Air quality prediction using a trained XGBoost model.",
    version="1.0.0",
)


# --------------------------------------------------
# 4. CORS CONFIGURATION
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# 5. LOAD TRAINED MODEL
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Trained XGBoost model not found: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# 6. LOAD MODEL METRICS
# --------------------------------------------------

metrics = {}

if METRICS_PATH.exists():
    with open(METRICS_PATH, "r", encoding="utf-8") as file:
        metrics = json.load(file)


# --------------------------------------------------
# 7. INPUT DATA VALIDATION
# --------------------------------------------------

class AirQualityInput(BaseModel):

    pt08_s1_co: float = Field(ge=0)
    pt08_s2_nmhc: float = Field(ge=0)
    pt08_s3_nox: float = Field(ge=0)
    pt08_s4_no2: float = Field(ge=0)
    pt08_s5_o3: float = Field(ge=0)

    temperature: float
    humidity: float = Field(ge=0, le=100)
    absolute_humidity: float = Field(ge=0)


# --------------------------------------------------
# 8. HOME ROUTE
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "success": True,
        "message": "Air Quality Intelligence ML API is running.",
        "model": "XGBoost Regressor",
    }


# --------------------------------------------------
# 9. HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "success": True,
        "service": "Air Quality Intelligence ML API",
        "model": "XGBoost Regressor",
        "status": "loaded",
        "features": FEATURES,
        "metrics": metrics,
    }


# --------------------------------------------------
# 10. AIR QUALITY PREDICTION
# --------------------------------------------------

@app.post("/predict")
def predict(data: AirQualityInput):

    try:

        input_values = {
            "PT08.S1(CO)": data.pt08_s1_co,
            "PT08.S2(NMHC)": data.pt08_s2_nmhc,
            "PT08.S3(NOx)": data.pt08_s3_nox,
            "PT08.S4(NO2)": data.pt08_s4_no2,
            "PT08.S5(O3)": data.pt08_s5_o3,
            "T": data.temperature,
            "RH": data.humidity,
            "AH": data.absolute_humidity,
        }

        input_df = pd.DataFrame(
            [input_values],
            columns=FEATURES,
        )

        prediction = float(model.predict(input_df)[0])

        return {
            "success": True,
            "model": "XGBoost Regressor",
            "target": "CO(GT)",
            "predicted_co": round(prediction, 4),
            "unit": "mg/m³",
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}",
        )


# --------------------------------------------------
# 11. MODEL INFORMATION
# --------------------------------------------------

@app.get("/model-info")
def model_info():

    return {
        "model": "XGBoost Regressor",
        "target": "CO(GT)",
        "features": FEATURES,
        "training_rows": metrics.get("training_rows"),
        "testing_rows": metrics.get("testing_rows"),
        "MAE": metrics.get("MAE"),
        "RMSE": metrics.get("RMSE"),
        "R2": metrics.get("R2"),
    }
