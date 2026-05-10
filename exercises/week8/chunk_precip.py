import sys
import pandas as pd

path = sys.argv[1]
chunk_size = int(sys.argv[2])

total = 0.0
for chunk in pd.read_csv(path, chunksize=chunk_size):
    mask = chunk["parameterId"].str.contains("precip", case=False, na=False)
    total += chunk.loc[mask, "value"].sum()

print(total)
