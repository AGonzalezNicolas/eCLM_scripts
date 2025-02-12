"""
Created on Tue Feb 12 2025

@author: Ana GNA

This script extracts data (number of cores and times) from a "csv" 
and plots speedup (measured and ideal) versus the number of cores

"""
import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
input_csv = "Output_times.csv"  # File to read with number of cores and times
data = pd.read_csv(input_csv)

# Extract number of cores and total time
num_cores = data["cores"].values
total_times = data["total_time"].values

# Find reference values (minimum number of cores)
ref_index = num_cores.argmin()  # Index of the lowest core count
num_cores_ref = num_cores[ref_index]
total_time_ref = total_times[ref_index]

# Compute speedup and ideal speedup
speedup = total_time_ref / total_times
ideal_speedup = num_cores / num_cores_ref

# Create square plot
plt.figure(figsize=(6, 6))  # Square figure

# Plot measured speedup (solid line with dots) in black
plt.plot(num_cores, speedup, "o-", label="Speedup", color="black", markersize=6)

# Plot ideal speedup (dashed line) also in black
plt.plot(num_cores, ideal_speedup, "--", label="Ideal Speedup", color="black")

# Labels and title
plt.xlabel("Number of Cores", fontsize=14)
plt.ylabel("Speedup", fontsize=14)
plt.title("eCLM Speedup vs. Number of Cores", fontsize=16)                ## Change title

# Formatting
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle="--", linewidth=0.5, color="gray")

# Save and show plot
plt.savefig("eCLM_strong_scaling_plot.png", dpi=300, bbox_inches="tight")  ## Change figure name
plt.show()
