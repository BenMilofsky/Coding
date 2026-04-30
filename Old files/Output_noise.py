import pandas as pd
import matplotlib.pyplot as plt

# --- Load CSV with 2-row header ---
df = pd.read_csv("TPS1_dirty.csv", header=[0, 1])

# --- Extract time column (assumes name is 'timestamp') ---
time = df[("timestamps", "s")]  # adjust unit if needed

# --- Choose which channels to plot ---
channels_to_plot = [
    ("CAN1.OBD2.S01PID11_ThrottlePosition", "%"),       # example: throttle percent
    ("CAN1.OBD2.S01PID05_EngineCoolantTemp", "%"),       # example: second TPS channel
]

# --- Plot ---
plt.figure()

for name, unit in channels_to_plot:
    if (name, unit) in df.columns:
        plt.plot(time, df[(name, unit)], label=f"{name} ({unit})")

plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.title("Selected Signals vs Time")
plt.legend()
plt.grid(True)

plt.show()