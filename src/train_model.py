
from pathlib import Path
import json

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "air_quality_cleaned.csv"
MODEL_DIR = PROJECT_DIR / "models"
REPORT_DIR = PROJECT_DIR / "reports"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load the cleaned dataset
df = pd.read_csv(DATA_FILE)

# Convert measurements to numeric values
for col in df.columns:
    if col not in ["Date", "Time", "Timestamp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

target = "CO(GT)"

if target not in df.columns:
    raise ValueError(
        f"Target {target} not found. Available columns: {df.columns.tolist()}"
    )

# Use sensor measurements and environmental conditions as features
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

features = [col for col in feature_candidates if col in df.columns]

if len(features) < 2:
    raise ValueError(f"Not enough usable features. Found: {features}")

# Keep rows with a known target value
model_data = df[features + [target]].copy()
model_data = model_data.replace([np.inf, -np.inf], np.nan)
model_data = model_data.dropna(subset=[target])

X = model_data[features]
y = model_data[target]

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Impute missing sensor readings and train the model
model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("regressor", RandomForestRegressor(
        n_estimators=150,
        random_state=42,
        n_jobs=-1
    )),
])

model.fit(X_train, y_train)

# Evaluate on unseen test data
predictions = model.predict(X_test)

metrics = {
    "model": "Random Forest Regressor",
    "target": target,
    "features": features,
    "training_rows": int(len(X_train)),
    "testing_rows": int(len(X_test)),
    "MAE": float(mean_absolute_error(y_test, predictions)),
    "RMSE": float(np.sqrt(mean_squared_error(y_test, predictions))),
    "R2": float(r2_score(y_test, predictions)),
}

# Save the trained model and evaluation report
model_path = MODEL_DIR / "co_random_forest.joblib"
report_path = REPORT_DIR / "model_metrics.json"

joblib.dump(model, model_path)

with open(report_path, "w", encoding="utf-8") as file:
    json.dump(metrics, file, indent=4)

print("Model training completed successfully!")
print(json.dumps(metrics, indent=4))
print("Model saved to:", model_path)
print("Metrics saved to:", report_path)
