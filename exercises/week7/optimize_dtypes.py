import pandas as pd

ZIP_PATH = "/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip"


def summarize_columns(df):
    print(pd.DataFrame([
        (
            c,
            df[c].dtype,
            len(df[c].unique()),
            df[c].memory_usage(deep=True) // (1024**2)
        ) for c in df.columns
    ], columns=['name', 'dtype', 'unique', 'size (MB)']))
    print('Total size:', df.memory_usage(deep=True).sum() / 1024**2, 'MB')


def reduce_dmi_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. Date types: parse date strings to datetime64
    df['created'] = pd.to_datetime(df['created'], format='ISO8601')
    df['observed'] = pd.to_datetime(df['observed'], format='ISO8601')

    # 2. Recode categoricals: replace repeated strings/ints with integer codes
    df['parameterId'] = df['parameterId'].astype('category')
    df['stationId'] = df['stationId'].astype('category')

    # 3. Smaller numeric types: float64 -> float32
    df['coordsx'] = df['coordsx'].astype('float32')
    df['coordsy'] = df['coordsy'].astype('float32')
    df['value'] = df['value'].astype('float32')

    return df


if __name__ == "__main__":
    df = pd.read_csv(ZIP_PATH)

    print("=== Before ===")
    summarize_columns(df)

    df_opt = reduce_dmi_df(df)

    print("\n=== After ===")
    summarize_columns(df_opt)

    before = df.memory_usage(deep=True).sum()
    after = df_opt.memory_usage(deep=True).sum()
    print(f"\nReduction: {before / 1024**2:.1f} MB -> {after / 1024**2:.1f} MB "
          f"({100 * (1 - after/before):.1f}% smaller)")
