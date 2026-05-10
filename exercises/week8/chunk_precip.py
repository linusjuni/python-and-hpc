import sys
import pandas as pd

path = sys.argv[1]
chunk_size = int(sys.argv[2])

total = 0.0
for chunk in pd.read_csv(path, chunksize=chunk_size):
    mask = chunk["parameterId"] == "precip_past1h"
    total += chunk.loc[mask, "value"].sum()

print(total)
