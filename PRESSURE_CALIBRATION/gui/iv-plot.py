import tkinter as tk
from tkinter import messagebox
import os
from Instruments import NanoVoltmeter, SourceMeter
import pyvisa
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
from utils import get_time, write_to_csv

import json
# Load the JSON file
with open('iv_config.json', 'r') as file:
    CONFIG = json.load(file)


# -------------------------------------------------------------------------------------
CSV_FILENAME = CONFIG['CSV_FILENAME']
MIN_MEASUREMENT_RANGE = CONFIG['MIN_MEASUREMENT_RANGE']
MAX_MEASUREMENT_RANGE = CONFIG['MAX_MEASUREMENT_RANGE']
MEASUREMENT_STEPS = CONFIG['MEASUREMENT_STEPS']
STEP_SIZE = (MAX_MEASUREMENT_RANGE - MIN_MEASUREMENT_RANGE) / MEASUREMENT_STEPS
MEASUREMENT_INTERVAL_SECS = CONFIG['MEASUREMENT_INTERVAL_SECS']
AVERAGE_COUNT_PER_MEASUREMENT = CONFIG['AVERAGE_COUNT_PER_MEASUREMENT']
START_TIMESTAMP = time.time()
EPSILON = CONFIG['EPSILON']


DEFAULT_CONFIG_VALUE = [CSV_FILENAME, MIN_MEASUREMENT_RANGE, MAX_MEASUREMENT_RANGE,
                        MEASUREMENT_STEPS, MEASUREMENT_INTERVAL_SECS, AVERAGE_COUNT_PER_MEASUREMENT]

headers = ['Timestamp', 'Current (A)', 'Voltage (V)', "Resistance (Ohm)"]

# -------------------------------------------------------------------------------------
currents = []
voltages = []
resistances = []

running_current = MIN_MEASUREMENT_RANGE

# -------------------------------------------------------------------------------------


def render(anim):
    global running_current, CSV_FILENAME
    if running_current > MAX_MEASUREMENT_RANGE:
        messagebox.showinfo(
            "Done", "Finished Measurement!")
        anim.event_source.stop()
        return

    sourcemeter.set_current(running_current)
    start_time = time.time()
    # ---------------------------------
    avg_volts = []
    for i in range(AVERAGE_COUNT_PER_MEASUREMENT):
        volt = nanovolt.measure_voltage()
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
    actual_filename = f"{CSV_FILENAME}-{START_TIMESTAMP}.csv"
    write_to_csv(actual_filename, headers, data)

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


def animate(frame,anim):
    render(anim)
    plt.cla()
    plt.plot(currents, voltages, c='lightblue', linestyle='dashed', zorder=1)
    plt.scatter(currents, voltages,
                label="Current vs Voltage", c='red', zorder=2)
    plt.legend()
    plt.tight_layout()


class UserInterface(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Instrument Control")
        self.pack(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        # Input frame for floats
        input_frame = tk.Frame(self)
        input_frame.pack(pady=5)

        self.entries = {}
        labels = ["CSV FILENAME", "MIN MEASUREMENT RANGE(A)", "MAX MEASUREMENT RANGE(A)", "MEASUREMENT STEPS",
                  "MEASUREMENT INTERVAL(s)", "AVERAGE COUNT PER MEASUREMENT"]
        for i, text in enumerate(labels):
            tk.Label(input_frame, text=text + ":").grid(row=i,
                                                        column=0, padx=5, pady=2, sticky="e")
            entry = tk.Entry(input_frame, width=10)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entry.insert(0, DEFAULT_CONFIG_VALUE[i])
            self.entries[text] = entry

        # Frame for LED indicators (simulated with Labels)
        led_frame = tk.Frame(self)
        led_frame.pack(pady=5)

        # Instrument 1 LED (top)
        self.instrument1_led = tk.Label(
            led_frame, text="NanoVoltmeter", bg="grey", fg="white", width=20, height=2)
        self.instrument1_led.pack(pady=(0, 5))

        # Instrument 2 LED (bottom)
        self.instrument2_led = tk.Label(
            led_frame, text="SourceMeter", bg="grey", fg="white", width=20, height=2)
        self.instrument2_led.pack(pady=(0, 5))

        # Start button
        self.start_button = tk.Button(
            self, text="Start", command=self.start_process,width=20,height=2)
        self.start_button.pack(pady=10)

    def start_process(self):
        global STEP_SIZE,CSV_FILENAME, MIN_MEASUREMENT_RANGE, MAX_MEASUREMENT_RANGE, MEASUREMENT_STEPS, MEASUREMENT_INTERVAL_SECS, AVERAGE_COUNT_PER_MEASUREMENT, running_current, currents, voltages, resistances,START_TIMESTAMP
        try:
            data = [entry.get() for label, entry in self.entries.items()]
            CSV_FILENAME = data[0]
            MIN_MEASUREMENT_RANGE = float(data[1])
            MAX_MEASUREMENT_RANGE = float(data[2])
            MEASUREMENT_STEPS = int(data[3])
            MEASUREMENT_INTERVAL_SECS = float(data[4])
            AVERAGE_COUNT_PER_MEASUREMENT = int(data[5])

            STEP_SIZE = (MAX_MEASUREMENT_RANGE - MIN_MEASUREMENT_RANGE) / MEASUREMENT_STEPS

            running_current = MIN_MEASUREMENT_RANGE
            currents = []
            voltages = []
            resistances = []
            START_TIMESTAMP = time.time()
        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter valid float numbers.")
            return

        # Start the process
        anim = FuncAnimation(
            plt.gcf(), animate, interval=100, cache_frame_data=False)
    
        # Pass the animation object to the animate function
        anim._args = (anim,)
        plt.show()
        


if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(master=root)

    # -------------------------------------------------------------------------------------

    # Setup pyVISA resource Manager
    rm = pyvisa.ResourceManager()
    try:
        nanovolt = NanoVoltmeter(rm, 'GPIB0::7::INSTR')
        app.instrument1_led.config(bg='lightgreen')
    except:
        app.instrument1_led.config(bg='red')
        messagebox.showerror(
            "Instrument Error", "Please make sure Instrument is plugged properly!")
    try:
        sourcemeter = SourceMeter(rm, 'GPIB0::18::INSTR')
        app.instrument2_led.config(bg='lightgreen')
    except:
        app.instrument2_led.config(bg='red')
        messagebox.showerror(
            "Instrument Error", "Please make sure Instrument is plugged properly!")
    app.mainloop()
