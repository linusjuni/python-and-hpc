import pandas as pd
import matplotlib.pyplot as plt

PATH = "/work3/s252653/python-and-hpc/miniproject/results/exercise11"

df = pd.read_csv(f"{PATH}/output.csv")
print(df.columns)

# Histogram of mean temperatures
plt.figure()
plt.hist(df["mean_temp"], bins=50)
plt.xlabel("Mean Temperature")
plt.ylabel("Number of Buildings")
plt.title("Distribution of Mean Temperatures")
plt.savefig(f"{PATH}/mean_temperatures.png")


avg_mean_temp = df["mean_temp"].mean()
avg_std_temp = df["std_temp"].mean()
count_above_18 = (df["pct_above_18"] >= 50).sum()
count_below_15 = (df["pct_below_15"] >= 50).sum()

df_summary = pd.DataFrame({
    "Average Mean Temperature": [avg_mean_temp],
    "Average Std Dev": [avg_std_temp],
    "Buildings >=50% Above 18°C": [count_above_18],
    "Buildings >=50% Below 15°C": [count_below_15]
})

df_summary.to_csv(f"{PATH}/summary_stats.csv", index=False)

print("Average mean temperature:", avg_mean_temp)
print("Average temperature std dev:", avg_std_temp)
print("Buildings with >=50% area above 18°C:", count_above_18)
print("Buildings with >=50% area below 15°C:", count_below_15)
