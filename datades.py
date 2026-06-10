import pandas as pd
import numpy as np

def analyse_dataset(csv_file):
    # Read CSV normally
    df = pd.read_csv(csv_file,header=[0,1])

    # Extract column names (row already handled by pandas)
    time =df['timestamps'].values #pandas
    time = np.asarray(time).flatten()
    time=np.ascontiguousarray(time)

    signal = df['CAN1.OBD2.S01PID11_ThrottlePosition'].values
    signal = np.asarray(signal).flatten()
    signal=np.ascontiguousarray(signal)

    # Ensure sorted by time (important for logs)
    sorted_idx = np.argsort(time)
    time = time[sorted_idx]
    signal = signal[sorted_idx]

    # Time differences
    dt = np.diff(time)
    dt = dt[dt > 0]  # remove invalid

    # Sampling frequency
    fs_inst = 1 / dt

    fs_avg = np.mean(fs_inst)
    fs_med = np.median(fs_inst)

    # Signal stats
    sig_min = np.min(signal)
    sig_max = np.max(signal)
    sig_mean = np.mean(signal)
    sig_std = np.std(signal)

    # Dataset duration
    duration = time[-1] - time[0]

    # Output report-style text
    report = f"""
DATASET SUMMARY
----------------
Samples: {len(time)}
Duration: {duration:.3f} s

SAMPLING FREQUENCY
-------------------
Med fs: {fs_med:.2f} Hz

Average fs: {fs_avg:.2f} Hz

SIGNAL STATISTICS
-------------------
Min value: {sig_min:.4f}
Max value: {sig_max:.4f}
Mean value: {sig_mean:.4f}
Standard deviation: {sig_std:.4f}
"""

    print(report)
    return report


# Example usage:
analyse_dataset("TPS2.csv")