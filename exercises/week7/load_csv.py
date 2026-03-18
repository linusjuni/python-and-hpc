import subprocess
import tempfile
import time
from pathlib import Path

import pandas as pd

ZIP_PATH = "/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip"


def approach1_unzip_then_read():
    """Unzip to a temp file, then read the CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(["unzip", "-q", ZIP_PATH, "-d", tmpdir], check=True)
        csv_file = next(Path(tmpdir).glob("*.csv"))
        df = pd.read_csv(csv_file)
    return df


def approach2_read_zip_directly():
    """Read the zip file directly with pandas."""
    df = pd.read_csv(ZIP_PATH)
    return df


def time_approach(name, fn):
    start = time.perf_counter()
    df = fn()
    elapsed = time.perf_counter() - start
    print(f"{name}: {elapsed:.3f}s  ({len(df):,} rows, {len(df.columns)} columns)")
    return elapsed


if __name__ == "__main__":
    t1 = time_approach("Approach 1 (unzip then read_csv)", approach1_unzip_then_read)
    t2 = time_approach("Approach 2 (read_csv from zip)  ", approach2_read_zip_directly)
    print(f"\nSpeedup (1/2): {t1/t2:.2f}x")
