#!/usr/bin/python

import numpy as np

def deep_water_length(T):
    """Calculate wave length for deep water conditions."""
    g = 9.81  # Gravitational acceleration (m/s^2)
    L = g * T**2 / (2. * np.pi) * 1000  # Convert to mm
    return L

# Input parameters (논문 조건 반영)
H = 148.6  # Wave height in mm
h = 661.0  # Water depth in mm (Deep Water 이론에서는 h가 무시됨)
T = 1.64   # Wave period in seconds
phase0 = 0.0
direction = 15.0  # Wave direction in degrees
nPaddles = 1
bLims = [0.0, 5000.0]  # Paddle boundary limits in mm
t0 = 0.0  # Simulation start time
tEnd = 31.0  # Simulation end time
dt = 0.005

# Calculations
L = deep_water_length(T)  # Wave length in mm
k = 2. * np.pi / L  # Wave number in mm^-1
w = 2. * np.pi / T  # Angular frequency in rad/s
S = H / 2.  # Stroke amplitude in mm

# 디버깅: 계산 값 출력
print(f"Deep Water Length (L): {L:.2f} mm")
print(f"Wave Number (k): {k:.6f} mm^-1")
print(f"Angular Frequency (w): {w:.6f} rad/s")
print(f"Stroke Amplitude (S): {S:.2f} mm")

# Generate time series and paddle coordinates
times = np.linspace(t0, tEnd, round((tEnd - t0) / dt) + 1)
coords = np.linspace(bLims[0], bLims[1], nPaddles + 1)
coords = coords[:-1] + np.diff(coords) / 2.

# Export wavemaker movement data
with open('wavemakerMovement.txt', 'w') as fid:
    fid.write('wavemakerType   Flap;\n')
    fid.write('tSmooth         1.5;\n')
    fid.write('genAbs          0;\n\n')

    # Write time series
    fid.write('timeSeries {0}(\n'.format(len(times)))
    for t in times:
        fid.write(f'{t:.5f}\n')
    fid.write(');\n\n')

    # Write paddle tilt angles
    fid.write('paddleTilt {0}(\n'.format(nPaddles))
    for i in range(nPaddles):
        fid.write(f'{len(times)}(\n')
        for t in times:
            x = S * np.cos(-w * t + np.pi / 2. + phase0 + 2. * np.pi * coords[i] / L * np.sin(direction * np.pi / 180.))
            theta = np.arctan(x / L) * 180. / np.pi  # Convert to degrees
            if np.isnan(theta):
                print(f"NaN detected in tilt angle at time {t:.5f}")
                theta = 0.0
            fid.write(f'{theta:.5f}\n')
        fid.write(')\n')
    fid.write(');\n\n')
