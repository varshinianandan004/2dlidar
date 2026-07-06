import serial
import re
import matplotlib.pyplot as plt
import numpy as np


SERIAL_PORT = 'com3'
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)

angles = []
distances = []

plt.ion()
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

print("Listening for scan data... (Ctrl+C to stop)")

try:
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            continue

        if "One full 360" in line:
            print("Scan complete. Plotting final result.")
            break

        match = re.match(r"Angle:\s*(\d+).*Distance:\s*(-?\d+)", line)
        if match:
            angle = int(match.group(1))
            distance = int(match.group(2))

            if distance == -1:
                continue  # skip out-of-range readings

            angles.append(np.radians(angle))
            distances.append(distance)

            # Live update
            ax.clear()
            ax.scatter(angles, distances, c='red', s=20)
            ax.set_title("2D LiDAR Scan (mm)")
            plt.pause(0.01)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    ser.close()
    plt.ioff()
    plt.show()
