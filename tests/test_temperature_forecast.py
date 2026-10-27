
import pandas as pd
import pytest

from src.forecasting.temperature_forecast import forecast_temperature


@pytest.fixture
def sample_climate_data():
    dates = pd.date_range(
        start="2010-01-01",
        periods=60,
        freq="MS",
    )

    temperatures = [
        25 + 0.03 * i + 3 * __import__("math").sin(2 * __import__("math").pi * i / 12)
        for i in range(60)
    ]

    return pd.DataFrame(
        {
            "date": dates,
            "temperature_c": temperatures,
        }
    )


def test_forecast_returns_requested_number_of_months(sample_climate_data):
    forecast = forecast_temperature(sample_climate_data, periods=12)

    assert len(forecast) == 12


def test_forecast_dates_and_values_are_valid(sample_climate_data):
    forecast = forecast_temperature(sample_climate_data, periods=12)

    expected_dates = pd.date_range(
        start="2015-01-01",
        periods=12,
        freq="MS",
    )

    assert forecast["date"].tolist() == expected_dates.tolist()
    assert forecast["forecast_temperature_c"].notna().all()


def test_forecast_rejects_zero_periods(sample_climate_data):
    with pytest.raises(ValueError, match="at least 1"):
        forecast_temperature(sample_climate_data, periods=0)


def test_forecast_rejects_empty_data():
    empty_data = pd.DataFrame(columns=["date", "temperature_c"])

    with pytest.raises(ValueError, match="empty dataset"):
        forecast_temperature(empty_data)
