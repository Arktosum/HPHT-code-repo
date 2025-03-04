import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from utils import get_time, write_to_csv

# Setup pyVISA resource Manager
rm = pyvisa.ResourceManager()

# Setup Nanovoltmeter with required settings
nano_volt = rm.open_resource('GPIB0::7::INSTR')
nano_volt.write('*RST')  # Reset Nanovoltmeter
# Set Nanovoltmeter to sense voltage
nano_volt.write(":SENS:FUNC 'VOLT'; :SENS:CHAN 1;:SENS:VOLT:RANG:AUTO ON")
# Setup Sourcemeter with required settings
sm = rm.open_resource('GPIB0::18::INSTR')
sm.write('*RST')  # Reset Nanovoltmeter
sm.write(":SOURce:FUNCtion CURRent")  # Set device to source current.
sm.query(":MEASure:VOLTage?")


# Get both the device names on succesful Connection
print(nano_volt.query("*IDN?"))
print(sm.query("*IDN?"))


def set_current(current):
    sm.write(f":SOUR:CURR {current}")
    sm.write(f":OUTP ON")


def measure_voltage(current: float):
    current = set_current(current)
    volt = float(nano_volt.query(":READ?"))
    time.sleep(0.5)
    return volt


MIN_RANGE = -500*10**-6
MAX_RANGE = +500*10**-6

STEP = 10
step_size = (MAX_RANGE - MIN_RANGE) / STEP
current = MIN_RANGE

MEASUREMENT_INTERVAL = 0
AVERAGE_COUNT = 5
epsilon = 1e-9
CURRENT_TIME = time.strftime("%Y-%m-%d_%H-%M-%S")
DATE = time.strftime("%d-%m-%Y")
csv_filename = f"./{DATE}/"+input("Enter the file name to write to: ") + ".csv"
while " " in csv_filename:
    print("There was a space in the file name! Try again!")
    csv_filename = f"./{DATE}/" + \
        input("Enter the file name to write to: ") + ".csv"

headers = ['Timestamp', 'Current (A)', 'Voltage (V)', "Resistance (Ohm)"]

currents = []
voltages = []
resistances = []


def render():
    global current
    if current > MAX_RANGE:
        print('Done with measurement!')
        return
    avg_volts = []
    for i in range(AVERAGE_COUNT):
        volt = measure_voltage(current)
        avg_volts.append(volt)

    # ---------------------------------
    avg_volt = sum(avg_volts)/len(avg_volts)
    resistance = avg_volt/(current + epsilon)
    # ---------------------------------
    currents.append(current)
    voltages.append(avg_volt)
    resistances.append(resistance)
    # ---------------------------------
    timestamp = get_time()
    data = [timestamp, current, avg_volt, resistance]
    write_to_csv(csv_filename, headers, data)

    print(f"-----------------------------")
    print(f"Timestamp : ", timestamp)
    print(f"Current : {current} A")
    print(f"Avg Voltage : {avg_volt} V")
    print(f"Resistance : {resistance} Ohm")
    print(f"-----------------------------")

    current += step_size
    time.sleep(MEASUREMENT_INTERVAL)
    # ---------------------------------


plt.style.use('fivethirtyeight')
time.sleep(0.01)


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
