
from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "air_quality_cleaned.csv"
MODEL_DIR = PROJECT_DIR / "models"
REPORT_DIR = PROJECT_DIR / "reports"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

# Convert sensor measurements to numeric values
for col in df.columns:
    if col not in ["Date", "Time", "Timestamp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

target = "CO(GT)"
feature_candidates = [
    "PT08.S1(CO)",
    "PT08.S2(NMHC)",
    "PT08.S3(NOx)",
    "PT08.S4(NO2)",
    "PT08.S5(O3)",
    "T",
    "RH",
    "AH",
]

if target not in df.columns:
    raise ValueError(f"Target column {target} was not found.")

features = [col for col in feature_candidates if col in df.columns]

if len(features) < 2:
    raise ValueError(f"Not enough usable features: {features}")

data = df[features + [target]].copy()
data = data.replace([np.inf, -np.inf], np.nan)
data = data.dropna(subset=[target])

X = data[features]
y = data[target]

# Use the same split as the Random Forest training script
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("regressor", XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1,
    )),
])

model.fit(X_train, y_train)
predictions = model.predict(X_test)

metrics = {
    "model": "XGBoost Regressor",
    "target": target,
    "features": features,
    "training_rows": int(len(X_train)),
    "testing_rows": int(len(X_test)),
    "MAE": float(mean_absolute_error(y_test, predictions)),
    "RMSE": float(np.sqrt(mean_squared_error(y_test, predictions))),
    "R2": float(r2_score(y_test, predictions)),
}

model_path = MODEL_DIR / "xgboost.joblib"
report_path = REPORT_DIR / "xgboost_metrics.json"

joblib.dump(model, model_path)

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(metrics, file, indent=4)

print("XGBoost training completed successfully!")
print(json.dumps(metrics, indent=4))
print("Model saved to:", model_path)
print("Metrics saved to:", report_path)
