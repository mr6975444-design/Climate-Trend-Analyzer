
from pathlib import Path

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def forecast_temperature(
    data: pd.DataFrame,
    periods: int = 12,
) -> pd.DataFrame:
    """
    Forecast monthly temperature using Holt-Winters smoothing.

    This model is intended for demonstration with synthetic data.
    It does not produce a real-world climate projection.
    """
    if periods < 1:
        raise ValueError("periods must be at least 1.")

    required_columns = {"date", "temperature_c"}
    missing_columns = required_columns.difference(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if data.empty:
        raise ValueError("Cannot forecast from an empty dataset.")

    monthly = data[["date", "temperature_c"]].copy()
    monthly["date"] = pd.to_datetime(monthly["date"])
    monthly = monthly.sort_values("date")

    if monthly["date"].duplicated().any():
        raise ValueError("Duplicate dates found in the dataset.")

    monthly = monthly.set_index("date")["temperature_c"].asfreq("MS")

    if monthly.isna().any():
        raise ValueError(
            "Temperature data contains missing values or missing months."
        )

    if len(monthly) < 36:
        raise ValueError(
            "At least 36 monthly observations are required."
        )

    model = ExponentialSmoothing(
        monthly,
        trend="add",
        seasonal="add",
        seasonal_periods=12,
        initialization_method="estimated",
    )

    fitted_model = model.fit(optimized=True)
    predictions = fitted_model.forecast(periods)

    forecast_dates = pd.date_range(
        start=monthly.index[-1] + pd.offsets.MonthBegin(1),
        periods=periods,
        freq="MS",
    )

    return pd.DataFrame(
        {
            "date": forecast_dates,
            "forecast_temperature_c": predictions.to_numpy(),
        }
    )


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    data_path = project_root / "data" / "raw" / "synthetic_climate_data.csv"
    output_path = (
        project_root / "outputs" / "reports" / "temperature_forecast.csv"
    )

    data = pd.read_csv(data_path, parse_dates=["date"])
    forecast = forecast_temperature(data, periods=12)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    forecast.to_csv(output_path, index=False)

    print("12-month synthetic temperature forecast:")
    print(forecast.to_string(index=False))
    print(f"\nForecast saved to: {output_path}")


if __name__ == "__main__":
    main()
