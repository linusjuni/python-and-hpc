import matplotlib.pyplot as plt

workers  = [1,    2,      4,      8,      16]
times    = [1139.88, 620.47, 410.27, 244.65, 177.64]
speedups = [times[0] / t for t in times]

plt.figure(figsize=(6, 4))
plt.plot(workers, speedups, 'o-', label='Measured')
plt.plot(workers, workers, '--', color='gray', label='Ideal')
plt.xlabel('Workers')
plt.ylabel('Speed-up')
plt.title('Task 5: Static Scheduling Speed-up (N=100)')
plt.legend()
plt.xticks(workers)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/exercise5/exercise5_speedup.png', dpi=150)
plt.show()