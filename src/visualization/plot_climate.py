
"""Generate charts for the Climate Trend Analyzer."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.load_data import load_climate_data
from src.analysis.climate_analysis import (
    calculate_yearly_averages,
    detect_temperature_anomalies,
)

FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"


def save_figure(filename: str) -> None:
    """Save the current chart as a high-resolution PNG."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(
        FIGURES_DIR / filename,
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()
    print(f"Saved: outputs/figures/{filename}")


def plot_yearly_temperature(yearly: pd.DataFrame) -> None:
    """Plot annual average temperature."""
    plt.figure(figsize=(10, 5))
    plt.plot(
        yearly["year"],
        yearly["temperature_c"],
        marker="o",
        label="Annual mean temperature",
    )
    plt.title("Annual Average Temperature (Synthetic Data)")
    plt.xlabel("Year")
    plt.ylabel("Temperature (°C)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    save_figure("yearly_temperature.png")


def plot_co2_and_sea_level(yearly: pd.DataFrame) -> None:
    """Plot annual CO2 and sea-level values on separate axes."""
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(
        yearly["year"],
        yearly["co2_ppm"],
        marker="o",
        label="CO2 concentration",
    )
    ax1.set_xlabel("Year")
    ax1.set_ylabel("CO2 (ppm)")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(
        yearly["year"],
        yearly["sea_level_mm"],
        marker="s",
        linestyle="--",
        label="Sea-level index",
    )
    ax2.set_ylabel("Sea-level index (mm)")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.title("Simulated CO2 and Sea-Level Trends")
    save_figure("co2_sea_level_trends.png")


def plot_monthly_seasonality(data: pd.DataFrame) -> None:
    """Show average temperature for each calendar month."""
    monthly = data.groupby("month")["temperature_c"].mean()

    plt.figure(figsize=(10, 5))
    plt.plot(
        monthly.index,
        monthly.values,
        marker="o",
    )
    plt.xticks(range(1, 13))
    plt.xlabel("Month")
    plt.ylabel("Average temperature (°C)")
    plt.title("Monthly Temperature Seasonality (Synthetic Data)")
    plt.grid(True, alpha=0.3)
    save_figure("monthly_temperature_seasonality.png")


def plot_temperature_anomalies(data: pd.DataFrame) -> None:
    """Plot temperature observations and flagged anomalies."""
    result = detect_temperature_anomalies(data)

    plt.figure(figsize=(12, 5))
    plt.plot(
        result["date"],
        result["temperature_c"],
        label="Monthly temperature",
        linewidth=1.2,
    )

    flagged = result[result["is_anomaly"]]

    plt.scatter(
        flagged["date"],
        flagged["temperature_c"],
        label="Flagged anomaly",
        zorder=3,
    )

    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Anomaly Detection (Synthetic Data)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    save_figure("temperature_anomalies.png")


def main() -> None:
    """Generate and save all project charts."""
    data = load_climate_data()
    yearly = calculate_yearly_averages(data)

    plot_yearly_temperature(yearly)
    plot_co2_and_sea_level(yearly)
    plot_monthly_seasonality(data)
    plot_temperature_anomalies(data)

    print("\nAll visualizations generated successfully!")


if __name__ == "__main__":
    main()
