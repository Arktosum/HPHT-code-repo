import os
from Instruments import NanoVoltmeter, SourceMeter
import pyvisa
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from utils import get_time, write_to_csv

import json
# Load the JSON file
with open('iv_config.json', 'r') as file:
    CONFIG = json.load(file)

# -------------------------------------------------------------------------------------

# Setup pyVISA resource Manager
rm = pyvisa.ResourceManager()
sourcemeter = SourceMeter(rm, 'GPIB1::18::INSTR')
# -------------------------------------------------------------------------------------

MIN_MEASUREMENT_RANGE = CONFIG['MIN_MEASUREMENT_RANGE']
MAX_MEASUREMENT_RANGE = CONFIG['MAX_MEASUREMENT_RANGE']
MEASUREMENT_STEPS = CONFIG['MEASUREMENT_STEPS']
STEP_SIZE = (MAX_MEASUREMENT_RANGE - MIN_MEASUREMENT_RANGE) / MEASUREMENT_STEPS
MEASUREMENT_INTERVAL_SECS = CONFIG['MEASUREMENT_INTERVAL_SECS']
AVERAGE_COUNT_PER_MEASUREMENT = CONFIG['AVERAGE_COUNT_PER_MEASUREMENT']
EPSILON = CONFIG['EPSILON']


# -------------------------------------------------------------------------------------
currents = []
voltages = []
resistances = []

running_current = MIN_MEASUREMENT_RANGE


def INITIALIZE():
    global currents, voltages, resistances, running_current
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
    running_current = MIN_MEASUREMENT_RANGE

    return csv_filename
# -------------------------------------------------------------------------------------

headers = ['Timestamp', 'Current (A)', 'Voltage (V)', "Resistance (Ohm)"]
csv_filename = INITIALIZE()

# -------------------------------------------------------------------------------------


def render():
    global running_current, csv_filename
    if running_current > MAX_MEASUREMENT_RANGE:
        print("Finished measuring!")
        choice = input('Continue measuring? [y/n]:')
        if choice == 'y':
            csv_filename = INITIALIZE()
        else:
            print('Done wil all measurements!')
            return

    sourcemeter.set_current(running_current)
    start_time = time.time()
    # ---------------------------------
    avg_volts = []
    for i in range(AVERAGE_COUNT_PER_MEASUREMENT):
        volt = sourcemeter.measure_voltage()
        avg_volts.append(volt)
    avg_volt = sum(avg_volts)/len(avg_volts)
    # ---------------------------------
    resistance = avg_volt/(running_current + EPSILON)
    # ---------------------------------
    currents.append(running_current)
    voltages.append(avg_volt)
    resistances.append(resistance)
    # ---------------------------------
    timestamp = get_time()
    data = [timestamp, running_current, avg_volt, resistance]
    write_to_csv(csv_filename, headers, data)

    # -------------- # Write to file --------------
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"-----------------------------")
    print(f"Timestamp : ", timestamp)
    print(f"Current : {running_current} A")
    print(f"Avg Voltage : {avg_volt} V")
    print(f"Resistance : {resistance} Ohm")
    print(f"Time taken : {elapsed_time} seconds")
    print(f"-----------------------------")

    running_current += STEP_SIZE
    time.sleep(MEASUREMENT_INTERVAL_SECS)
    # ---------------------------------


plt.style.use('fivethirtyeight')
time.sleep(0.01)
# -------------------------------------------------------------------------------------


def animate(i):
    render()
    plt.cla()
    plt.plot(currents, voltages, c='lightblue', linestyle='dashed', zorder=1)
    plt.scatter(currents, voltages,
                label="Current vs Voltage", c='red', zorder=2)
    plt.legend()
    plt.tight_layout()


plot_animation = FuncAnimation(
    plt.gcf(), animate, interval=100, cache_frame_data=False)
plt.show()
