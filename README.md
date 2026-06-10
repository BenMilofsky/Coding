Sensor Data Filtering and Visualisation Tool
Overview

The project consists of two main components:

Filters Module (Filters.py)

Contains signal filtering functions (Hybrid deadband and Butterworth).

GUI Application (Main_interface.py)

Allows users to import sensor data from CSV files.
Select filter and parameters.
Plot raw and filtered datasets

File Structure
Project Folder
│
├── Filters.py
├── Sensor_GUI.py
├── TPS1_Dirty.csv
└── README.md



Butterworth Filter

Function:
Butterworth(data, Order, Critical_frequency)

Description:
Applies a low-pass Butterworth filter to remove high-frequency noise from a signal.

The normalised cutoff frequency is:
Wn = fc / (fs / 2)

Where:
fc = desired cutoff frequency
fs = sampling frequency


Deadband Filter:

Function:
deadband(row, thresh)

Description:
Reduces small fluctuations and jitter in sensor signals.


Moving Average Filter:

Function:
movingaverage(data, MA_coeff)

Description:
Smooths data using a moving average window.

Formula:
y[n] = (x[n] + x[n−1] + ... + x[n−M+1]) / M

Where:
M = moving average coefficient



Main_interface.py

Purpose:
Provides a graphical user interface for importing data, selecting filters, and plotting results.

Features:
Import CSV Data

The application reads sensor data from:
TPS1_Dirty.csv

Sensor Selection:
Users can:
Select which sensor channels to import.

Filter Selection:
For each sensor channel the user can enable:

Deadband Filter:
Inputs:
Threshold value

Butterworth Filter:
Inputs:
Filter order
Critical frequency


Plotting:
The application displays:
Raw sensor data
Deadband filtered data
Butterworth filtered data

using Matplotlib embedded inside Tkinter.

Plot Controls:
Users can:
Select which signals to display.
Add diffrent plots
Zoom and pan using the Matplotlib toolbar.


Filter Parameters:
Butterworth Variables:
fs = 22
fp = 3
fsb = 5
ap = 0.5
As = 60
N = 16
Variable	Description
fs	Sampling frequency (Hz)
fp	Passband frequency (Hz)
fsb	Stopband frequency (Hz)
ap	Passband ripple (dB)
As	Stopband attenuation (dB)
N	Filter order
Definitions

Passband frequency:
fp = highest frequency passed with minimal attenuation

Stopband frequency:
fsb = frequency where strong attenuation begins

Passband ripple:
ap = allowable variation within passband

Stopband attenuation:
As = minimum attenuation in stopband

Filter order:
N = complexity of filter (IIR/No.coeffFIR)


Required Libraries:
Install required packages using:
pip install numpy pandas scipy matplotlib
Tkinter is included with most Python installations.

Running the Program:
Run the GUI using:
python main_interface.py

The application will:
Load the CSV file.
Allow sensor selection.
Apply selected filters.
Display results in a new plotting tab.
Typical Workflow
Open the application.
Select sensor channels.
Click Import.
Enable desired filters.
Enter filter parameters.
Click plot.
Choose what values to plot.
Click plot.

