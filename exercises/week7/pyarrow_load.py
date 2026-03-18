import time
import zipfile

import pandas as pd
import pyarrow.csv as pa_csv

ZIP_PATH = "/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip"


def pyarrow_load(path):
    """Load a CSV file using PyArrow and return the PyArrow table."""
    return pa_csv.read_csv(path)


def time_approach(name, fn):
    start = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    return elapsed, result


if __name__ == "__main__":
    # Pandas baseline (same as exercise 1, approach 2)
    t_pandas, df = time_approach("pandas", lambda: pd.read_csv(ZIP_PATH))
    print(f"Pandas:  {t_pandas:.3f}s  ({len(df):,} rows, {len(df.columns)} columns)")

    # PyArrow — unzip on the fly via zipfile, then pass the file object
    def load_arrow():
        with zipfile.ZipFile(ZIP_PATH) as z:
            with z.open(z.namelist()[0]) as f:
                return pa_csv.read_csv(f)

    t_arrow, table = time_approach("pyarrow", load_arrow)
    print(f"PyArrow: {t_arrow:.3f}s  ({table.num_rows:,} rows, {table.num_columns} columns)")

    print(f"\nSpeedup (pandas / pyarrow): {t_pandas / t_arrow:.2f}x")
