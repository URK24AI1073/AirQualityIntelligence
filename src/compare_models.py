
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
OUTPUTS = ROOT / "outputs"

OUTPUTS.mkdir(parents=True, exist_ok=True)

with open(REPORTS / "model_metrics.json", "r") as file:
    rf = json.load(file)

with open(REPORTS / "xgboost_metrics.json", "r") as file:
    xgb = json.load(file)

comparison = pd.DataFrame([
    {
        "Model": "Random Forest",
        "MAE": rf["MAE"],
        "RMSE": rf["RMSE"],
        "R2": rf["R2"]
    },
    {
        "Model": "XGBoost",
        "MAE": xgb["MAE"],
        "RMSE": xgb["RMSE"],
        "R2": xgb["R2"]
    }
])

print("\nMODEL COMPARISON")
print(comparison.to_string(index=False))

comparison.to_csv(
    OUTPUTS / "model_comparison.csv",
    index=False
)

metrics = ["MAE", "RMSE", "R2"]

fig, axes = plt.subplots(1, 3, figsize=(13, 4))

for ax, metric in zip(axes, metrics):
    ax.bar(comparison["Model"], comparison[metric])
    ax.set_title(metric)
    ax.set_ylabel("Score")
    ax.tick_params(axis="x", rotation=15)

plt.tight_layout()
plt.savefig(OUTPUTS / "model_comparison.png", dpi=300)
plt.close()

print("\nSaved:")
print("outputs/model_comparison.csv")
print("outputs/model_comparison.png")
