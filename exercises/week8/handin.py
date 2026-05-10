import sys
import pandas as pd

csv_path = sys.argv[1]
chunk_size = int(sys.argv[2])

total = 0.0
for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
    total += chunk[chunk['parameterId'] == 'precip_past10min']['value'].sum()

print(total)
