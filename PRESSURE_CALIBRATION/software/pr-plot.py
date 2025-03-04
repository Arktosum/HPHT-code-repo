import os
from Instruments import NanoVoltmeter, SourceMeter
import pyvisa
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from utils import get_time, write_to_csv

import json
# Load the JSON file
with open('pr_config.json', 'r') as file:
    CONFIG = json.load(file)

# -------------------------------------------------------------------------------------
# Setup pyVISA resource Manager
rm = pyvisa.ResourceManager()
nanovolt = NanoVoltmeter(rm, 'GPIB1::7::INSTR')
sourcemeter = SourceMeter(rm, 'GPIB1::18::INSTR')
# -------------------------------------------------------------------------------------

SOURCE_CURRENT = CONFIG['SOURCE_CURRENT']
MEASUREMENT_INTERVAL_SECS = CONFIG['MEASUREMENT_INTERVAL_SECS']
AVERAGE_COUNT_PER_MEASUREMENT = CONFIG['AVERAGE_COUNT_PER_MEASUREMENT']
EPSILON = CONFIG['EPSILON']

# -------------------------------------------------------------------------------------
currents = []
voltages = []
resistances = []
pressures = []


def INITIALIZE():
    global currents, voltages, resistances, pressures
    DATE = time.strftime("%d-%m-%Y")
    os.makedirs(DATE, exist_ok=True)
    csv_filename = f"./{DATE}/" + \
        input("Enter the file name to write to: ") + ".csv"
    while " " in csv_filename:
        print("There was a space in the file name! Try again!")
        csv_filename = f"./{DATE}/" + \
            input("Enter the file name to write to: ") + ".csv"

    currents = []
    voltages = []
    resistances = []
    pressures = []

    return csv_filename
# -------------------------------------------------------------------------------------


headers = ['Timestamp', 'Current (A)', 'Voltage (V)', "Resistance (Ohm)"]
csv_filename = INITIALIZE()

# -------------------------------------------------------------------------------------


def render():
    global csv_filename
    try:
        pressure = float(input('Enter External Load (bar) : '))
    except:
        print("Invalid Input, please try again.")
        return

    start_time = time.time()
    # ------------- Measure average voltage using the instrument --------------
    avg_volts = []
    for i in range(AVERAGE_COUNT_PER_MEASUREMENT):
        sourcemeter.set_current(-SOURCE_CURRENT)
        min_volt = nanovolt.measure_voltage()
        sourcemeter.set_current(SOURCE_CURRENT)
        max_volt = nanovolt.measure_voltage()
        volt = (abs(min_volt) + abs(max_volt)) / 2
        avg_volts.append(volt)

    # --------------------------------------------------------
    avg_volt = sum(avg_volts)/len(avg_volts)
    resistance = (avg_volt/(SOURCE_CURRENT+EPSILON))
    # ------------- Append to the dataset --------------
    resistances.append(resistance)
    voltages.append(avg_volt)
    pressures.append(pressure)
    # -------------- # Write to file --------------
    timestamp = get_time()
    data = [timestamp, pressure, avg_volt, resistance]
    write_to_csv(csv_filename, headers, data)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"-----------------------------")
    print(f"Timestamp : ", timestamp)
    print(f"External Load : {pressure} bar")
    print(f"Avg Voltage : {avg_volt} V")
    print(f"Resistance : {resistance} Ohm")
    print(f"Time taken : {elapsed_time} seconds")
    print(f"-----------------------------")


plt.style.use('fivethirtyeight')
time.sleep(0.01)
# -------------------------------------------------------------------------------------


def animate(i):
    render()
    plt.cla()
    plt.plot(pressures, resistances, c='lightblue', linestyle='dashed', zorder=1)
    plt.scatter(pressures, resistances,
                label="Resistance vs Pressure", c='red', zorder=2)
    plt.legend()
    plt.tight_layout()


plot_animation = FuncAnimation(
    plt.gcf(), animate, interval=100, cache_frame_data=False)
plt.show()
