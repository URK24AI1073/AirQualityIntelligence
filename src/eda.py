
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "air_quality_cleaned.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
REPORT_DIR = PROJECT_DIR / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load the cleaned dataset
df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)
print("\nFirst five rows:")
print(df.head())

# Identify numeric columns
numeric_df = df.select_dtypes(include="number")

# Create an EDA report
report = [
    "AIR QUALITY DATASET - EDA REPORT",
    "=" * 40,
    f"Rows: {len(df)}",
    f"Columns: {len(df.columns)}",
    "\nMissing values by column:",
    df.isna().sum().to_string(),
    "\nNumeric summary:",
    numeric_df.describe().round(3).to_string(),
]

report_text = "\n".join(report)
report_path = REPORT_DIR / "eda_report.txt"
report_path.write_text(report_text, encoding="utf-8")

print("\nMissing values:")
print(df.isna().sum())

# Plot 1: Missing values
missing = df.isna().sum()
missing = missing[missing > 0].sort_values(ascending=False)

if not missing.empty:
    plt.figure(figsize=(12, 6))
    missing.plot(kind="bar")
    plt.title("Missing Values by Column")
    plt.ylabel("Number of Missing Values")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "missing_values.png", dpi=150)
    plt.close()

# Plot 2: Histograms of numeric columns
if not numeric_df.empty:
    numeric_df.hist(figsize=(15, 12), bins=30)
    plt.suptitle("Air Quality Measurement Distributions")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "distributions.png", dpi=150)
    plt.close()

# Plot 3: Correlation heatmap
if numeric_df.shape[1] >= 2:
    plt.figure(figsize=(12, 9))
    sns.heatmap(
        numeric_df.corr(),
        cmap="coolwarm",
        center=0,
        annot=False
    )
    plt.title("Air Quality Feature Correlations")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "correlation_heatmap.png", dpi=150)
    plt.close()

# Plot 4: CO measurements over time
if "Timestamp" in df.columns and "CO(GT)" in df.columns:
    time_df = df[["Timestamp", "CO(GT)"]].copy()
    time_df["Timestamp"] = pd.to_datetime(
        time_df["Timestamp"], errors="coerce"
    )
    time_df["CO(GT)"] = pd.to_numeric(
        time_df["CO(GT)"], errors="coerce"
    )
    time_df = time_df.dropna().sort_values("Timestamp")

    if not time_df.empty:
        plt.figure(figsize=(14, 5))
        plt.plot(
            time_df["Timestamp"],
            time_df["CO(GT)"],
            linewidth=0.8
        )
        plt.title("Carbon Monoxide Measurements Over Time")
        plt.xlabel("Timestamp")
        plt.ylabel("CO(GT)")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "co_over_time.png", dpi=150)
        plt.close()

print("\nEDA completed successfully!")
print("Report saved to:", report_path)
print("Charts saved in:", OUTPUT_DIR)
