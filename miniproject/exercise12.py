"""
Task 12 — Analyse simulation results for all floorplans using Pandas.

Usage:
    python exercise12.py <csv_path>

Questions answered:
    a) Distribution of mean temperatures (histogram)
    b) Average mean temperature across all buildings
    c) Average temperature standard deviation across all buildings
    d) Number of buildings with >= 50% area above 18°C
    e) Number of buildings with >= 50% area below 15°C
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main(csv_path: str) -> None:
    df = pd.read_csv(csv_path, skipinitialspace=True)

    # --- b) Average mean temperature ---
    avg_mean_temp = df["mean_temp"].mean()
    print(f"b) Average mean temperature:          {avg_mean_temp:.4f} °C")

    # --- c) Average temperature standard deviation ---
    avg_std_temp = df["std_temp"].mean()
    print(f"c) Average temperature std deviation: {avg_std_temp:.4f} °C")

    # --- d) Buildings with >= 50% area above 18°C ---
    n_above_18 = (df["pct_above_18"] >= 50).sum()
    print(f"d) Buildings with ≥50%% area above 18°C: {n_above_18}")

    # --- e) Buildings with >= 50% area below 15°C ---
    n_below_15 = (df["pct_below_15"] >= 50).sum()
    print(f"e) Buildings with ≥50%% area below 15°C: {n_below_15}")

    # --- a) Histogram of mean temperatures ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].hist(df["mean_temp"], bins=40, edgecolor="black")
    axes[0].set_xlabel("Mean Temperature (°C)")
    axes[0].set_ylabel("Number of Buildings")
    axes[0].set_title("Distribution of Mean Temperatures")
    axes[0].axvline(avg_mean_temp, color="red", linestyle="--", label=f"Mean = {avg_mean_temp:.2f}°C")
    axes[0].legend()

    axes[1].hist(df["std_temp"], bins=40, edgecolor="black", color="steelblue")
    axes[1].set_xlabel("Temperature Std Deviation (°C)")
    axes[1].set_ylabel("Number of Buildings")
    axes[1].set_title("Distribution of Temperature Std Deviations")
    axes[1].axvline(avg_std_temp, color="red", linestyle="--", label=f"Mean std = {avg_std_temp:.2f}°C")
    axes[1].legend()

    plt.tight_layout()
    out_path = str(Path(csv_path).with_stem(Path(csv_path).stem + "_histograms").with_suffix(".png"))
    plt.savefig(out_path, dpi=150)
    print(f"\na) Histograms saved to {out_path}")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exercise12.py <csv_path>")
        sys.exit(1)
    main(sys.argv[1])
