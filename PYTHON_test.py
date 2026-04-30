import time
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt

t0 = time.time()

data = pd.read_csv('TPS2.csv')
signal = data['CAN1.OBD2.S01PID11_ThrottlePosition'].values
signal = np.asarray(signal).flatten()
signal = np.ascontiguousarray(signal)
b, a = butter(2, 0.45)
y = filtfilt(b, a, signal)

print(time.time() - t0)


