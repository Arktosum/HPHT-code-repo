import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
from utils import get_time, write_to_csv
from matplotlib.animation import FuncAnimation

import csv
rm = pyvisa.ResourceManager()
nano_volt = rm.open_resource('GPIB0::7::INSTR')
nano_volt.write('*RST')
nano_volt.write(":SENS:FUNC 'VOLT'; :SENS:CHAN 1;")
sm = rm.open_resource('GPIB0::18::INSTR')


def set_current(current):
    sm.write(f":SOUR:CURR {current}")
    sm.write(f":OUTP ON")


def measure_voltage(current: float):
    current = set_current(current)
    volt = float(nano_volt.query(":READ?"))
    time.sleep(1)
    return volt


CURRENT_TIME = time.strftime("%Y-%m-%d_%H-%M-%S")
DATE = time.strftime("%d-%m-%Y")
csv_filename = f"./{DATE}/"+input("Enter the file name to write to: ") + ".csv"
while " " in csv_filename:
    print("There was a space in the file name! Try again!")
    csv_filename = f"./{DATE}/"+input("Enter the file name to write to: ") + ".csv"

headers = ['Timestamp', 'Voltage (V)', 'Resistance (ohm)']
epsilon = 1e-9
AVERAGE_COUNT = 5
pressure = 0


current = 500*10**-6

resistances = []
voltages = []
pressures = []
timestamps = []

# # Open the CSV file
# with open(csv_filename, mode='r') as file:
#     csv_reader = csv.reader(file)

#     for timestamp, pressure, voltage, resistance in list(csv_reader)[1:]:
#         resistances.append(float(resistance))
#         voltages.append(float(voltage))
#         pressures.append(float(pressure))


def render():
    # ------------- Measure average voltage using the instrument --------------
    avg_volts = []
    for i in range(AVERAGE_COUNT):
        min_volt = measure_voltage(-current)
        max_volt = measure_voltage(current)
        volt = (abs(min_volt) + abs(max_volt)) / 2
        avg_volts.append(volt)

    avg_volt = sum(avg_volts)/len(avg_volts)
    resistance = (avg_volt/(current+epsilon))
    # ------------- Append to the dataset --------------
    resistances.append(resistance)
    voltages.append(avg_volt)
    pressures.append(pressure)
    # -------------- # Write to file --------------
    timestamp = get_time()
    timestamps.append(timestamp)
    data = [timestamp,avg_volt, resistance]
    write_to_csv(csv_filename, headers, data)
    print(f"-----------------------------")
    print(f"Timestamp : ", timestamp)
    print(f"Pressure : {pressure} bar")
    print(f"Avg Voltage : {avg_volt} V")
    print(f"Resistance : {resistance} Ohm")
    print(f"-----------------------------")


plt.style.use('fivethirtyeight')
time.sleep(0.01)


def animate(i):
    render()
    plt.cla()
    plt.plot(timestamps, resistances, c='lightblue',
             linestyle='dashed', zorder=1)
    plt.scatter(timestamps, resistances,
                label="Pressure vs Resistance", c='red', zorder=2)
    plt.legend()
    plt.tight_layout()


plot_animation = FuncAnimation(
    plt.gcf(), animate, interval=1000, cache_frame_data=False)
plt.show()
