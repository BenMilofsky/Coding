import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- User settings ---
input_file  = "TPS1.csv"
output_file = "TPS1_dirty.csv"
timestamp_col = "timestamp"   # name of your timestamp column
noise_std = 0.02              # noise level

# --- Read CSV (keep header rows as normal) ---
# row 1 = header, row 2 = units -> treat both as header
df = pd.read_csv(input_file, header=[0, 1])

# Replaces empty with empty string
df.columns = pd.MultiIndex.from_tuples(
    [(name, unit if isinstance(unit, str) else "") 
     for name, unit in df.columns]
)

# Separate names + units
col_names = df.columns.get_level_values(0)
col_units = df.columns.get_level_values(1)

# Convert data rows (3rd row onward) to numeric
data = df.copy()

# Loop through columns and add noise except timestamp
for i, col in enumerate(col_names):
    if col != timestamp_col:
        # Add noise only to numeric data rows
        try:
            numeric_vals = pd.to_numeric(data[(col, col_units[i])], errors='coerce')
            noise = np.random.normal(0, noise_std, size=len(numeric_vals))
            data[(col, col_units[i])] = numeric_vals + noise
        except:
            pass  # skip non-numeric columns

# --- Save CSV with same multi-row header format ---
data.to_csv(output_file, index=False)





print("Noisy file saved to:", output_file)

