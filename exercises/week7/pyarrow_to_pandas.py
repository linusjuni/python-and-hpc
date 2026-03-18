import time
import zipfile

import pandas as pd
import pyarrow.csv as pa_csv

ZIP_PATH = "/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip"


def pyarrow_load(path) -> pd.DataFrame:
    """Load a CSV file using PyArrow and return a pandas DataFrame."""
    return pa_csv.read_csv(path).to_pandas()


def time_approach(name, fn):
    start = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    return elapsed, result


if __name__ == "__main__":
    # Pandas baseline
    t_pandas, df = time_approach("pandas", lambda: pd.read_csv(ZIP_PATH))
    print(f"Pandas:           {t_pandas:.3f}s  ({len(df):,} rows, {len(df.columns)} columns)")

    # PyArrow — time read and conversion separately
    def load_arrow_zip():
        with zipfile.ZipFile(ZIP_PATH) as z:
            with z.open(z.namelist()[0]) as f:
                return pa_csv.read_csv(f)

    t_arrow, table = time_approach("PyArrow read_csv", load_arrow_zip)
    print(f"PyArrow read_csv: {t_arrow:.3f}s  ({table.num_rows:,} rows, {table.num_columns} columns)")

    t_convert, df_arrow = time_approach("to_pandas()", lambda: table.to_pandas())
    print(f"to_pandas():      {t_convert:.3f}s")

    t_total = t_arrow + t_convert
    print(f"\nPyArrow total (read + convert): {t_total:.3f}s")
    print(f"Speedup vs pandas — PyArrow only: {t_pandas / t_arrow:.2f}x")
    print(f"Speedup vs pandas — total:        {t_pandas / t_total:.2f}x")

    mb_pandas = df.memory_usage(deep=True).sum() / 1024**2
    mb_arrow  = table.nbytes / 1024**2
    mb_converted = df_arrow.memory_usage(deep=True).sum() / 1024**2
    print(f"\nMemory — pandas DataFrame:       {mb_pandas:.1f} MB")
    print(f"Memory — PyArrow table:          {mb_arrow:.1f} MB")
    print(f"Memory — converted DataFrame:    {mb_converted:.1f} MB")
