
from src.data.load_data import load_climate_data
from src.analysis.climate_analysis import (
    calculate_yearly_averages,
    calculate_temperature_trend,
    detect_temperature_anomalies,
)


def test_yearly_averages():
    data = load_climate_data()
    yearly = calculate_yearly_averages(data)

    assert not yearly.empty
    assert "year" in yearly.columns
    assert "temperature_c" in yearly.columns
    assert yearly["year"].is_monotonic_increasing


def test_temperature_trend():
    data = load_climate_data()
    trend = calculate_temperature_trend(data)

    assert "slope_c_per_year" in trend
    assert "slope_c_per_decade" in trend
    assert "r_squared" in trend
    assert "p_value" in trend
    assert -1 <= trend["r_squared"] <= 1
    assert 0 <= trend["p_value"] <= 1


def test_temperature_anomalies():
    data = load_climate_data()
    anomalies = detect_temperature_anomalies(data)

    assert "date" in anomalies.columns
    assert "temperature_c" in anomalies.columns
    assert "anomaly_score" in anomalies.columns
    assert "is_anomaly" in anomalies.columns
    assert anomalies["is_anomaly"].all()
