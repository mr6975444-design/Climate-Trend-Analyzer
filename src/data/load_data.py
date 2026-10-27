
"""Load and validate the Climate Trend Analyzer dataset."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "synthetic_climate_data.csv"
)

REQUIRED_COLUMNS = [
    "date",
    "year",
    "month",
    "temperature_c",
    "rainfall_mm",
    "humidity_percent",
    "co2_ppm",
    "sea_level_mm",
]


def load_climate_data() -> pd.DataFrame:
    """Load the climate dataset and validate its structure."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Run: python src/data/generate_data.py"
        )

    data = pd.read_csv(DATA_PATH, parse_dates=["date"])

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing columns: {missing_columns}"
        )

    if data.empty:
        raise ValueError("The climate dataset is empty.")

    if data["date"].isna().any():
        raise ValueError("The dataset contains invalid dates.")

    if data["date"].duplicated().any():
        raise ValueError("The dataset contains duplicate dates.")

    if data[REQUIRED_COLUMNS[3:]].isna().any().any():
        raise ValueError(
            "The climate measurements contain missing values."
        )

    if not data["month"].between(1, 12).all():
        raise ValueError("Month values must be between 1 and 12.")

    if not data["humidity_percent"].between(0, 100).all():
        raise ValueError("Humidity must be between 0 and 100.")

    print("Dataset loaded and validated successfully!")
    print(f"File: {DATA_PATH}")
    print(f"Rows: {len(data)}")
    print(f"Columns: {len(data.columns)}")
    print(f"Date range: {data['date'].min().date()} to "
          f"{data['date'].max().date()}")
    print(f"Missing values: {int(data.isna().sum().sum())}")
    print(f"Duplicate dates: {int(data['date'].duplicated().sum())}")

    return data


if __name__ == "__main__":
    climate_data = load_climate_data()

    print("\nPreview:")
    print(climate_data.head())
