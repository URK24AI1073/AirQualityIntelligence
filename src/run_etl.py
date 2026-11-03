from pathlib import Path
import subprocess
import sys
PROJECT_DIR = Path(__file__).resolve().parent.parent
CLEAN_SCRIPT = PROJECT_DIR / "src" / "clean_data.py"
OUTPUT_FILE = PROJECT_DIR / "data" / "processed" / "air_quality_cleaned.csv"
print("Starting Air Quality ETL pipeline...")
result = subprocess.run(
    [sys.executable, str(CLEAN_SCRIPT)],
    cwd=PROJECT_DIR
)
if result.returncode != 0:
    raise SystemExit("ETL pipeline failed during cleaning.")
if not OUTPUT_FILE.exists():
    raise FileNotFoundError("Processed dataset was not generated.")
print("ETL pipeline completed successfully!")
print("Output:", OUTPUT_FILE)
