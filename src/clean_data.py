
from pathlib import Path
import pandas as pd

# Project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Find the original dataset
csv_file = RAW_DIR / "AirQualityUCI.csv"
excel_file = RAW_DIR / "AirQualityUCI.xlsx"

if csv_file.exists():
    df = pd.read_csv(csv_file, sep=";", decimal=",")
elif excel_file.exists():
    df = pd.read_excel(excel_file)
else:
    raise FileNotFoundError(
        "AirQualityUCI.csv or AirQualityUCI.xlsx was not found "
        "inside data/raw. Please place the dataset there."
    )

# Remove completely empty columns and rows
df = df.dropna(axis=1, how="all")
df = df.dropna(axis=0, how="all")

# Clean column names
df.columns = df.columns.str.strip()

# Replace missing-value markers
df = df.replace(-200, float("nan"))
df = df.replace(-200.0, float("nan"))

# Combine date and time when both columns exist
if "Date" in df.columns and "Time" in df.columns:
    df["Timestamp"] = pd.to_datetime(
        df["Date"].astype(str).str.strip()
        + " "
        + df["Time"].astype(str).str.strip(),
        dayfirst=True,
        errors="coerce"
    )

# Save the cleaned dataset
output_file = PROCESSED_DIR / "air_quality_cleaned.csv"
df.to_csv(output_file, index=False)

print("Data cleaning completed successfully!")
print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Saved to:", output_file)