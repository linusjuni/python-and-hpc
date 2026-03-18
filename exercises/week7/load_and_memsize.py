import pandas as pd

ZIP_PATH = "/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip"


def df_memsize(df: pd.DataFrame) -> int:
    """Return the memory usage of a DataFrame in bytes."""
    return df.memory_usage(deep=True).sum()


if __name__ == "__main__":
    df = pd.read_csv(ZIP_PATH)
    size = df_memsize(df)
    print(f"Shape:       {df.shape}")
    print(f"Memory size: {size:,} bytes ({size / 1024**2:.1f} MB)")
