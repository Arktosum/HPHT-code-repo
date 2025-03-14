import pyodbc
import pandas as pd
import time
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from utils import get_time, write_to_csv
from matplotlib.animation import FuncAnimation

def set_current(current):
    sm.write(f":SOUR:CURR {current}")
    sm.write(f":OUTP ON")


def measure_voltage(current: float):
    set_current(current)
    volt = float(nano_volt.query(":READ?"))
    time.sleep(1)
    return volt


def setup_server():
    SERVER = 'IIT300T,1433'
    DATABASE = 'IIT300'
    USERNAME = 'bhipl'
    PASSWORD = 'bhipl100'
    connectionString = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};'
    conn = pyodbc.connect(connectionString)
    print("Connection established!")
    cursor = conn.cursor()
    return [conn, cursor]


MAP = [
    "ID",
    "DATE1",
    "TIME1",
    "BATCHNO",
    "RECEIPENAME",
    "ACKPOSITIONCH1",
    "ACKPOSITIONCH2",
    "ACKPOSITIONCH3",
    "ACKPOSITIONCH4",
    "ACKPOSITIONCH5",
    "ACKPOSITIONCH6",
    "ACKPOSITIONCH7",
    "ACKPOSITIONCH8",
    "HYDPRESSURE1",
    "HYDPRESSURE2",
    "HYDPRESSURE3",
    "HYDPRESSURE4",
    "HYDPRESSURE5",
    "HYDPRESSURE6",
    "HYDPRESSURE7",
    "HYDPRESSURE8",
    "VOLTAGE",
    "ICURRENT",
    "POWER",
    "POWERSPARE1",
    "CWTZ01",
    "CWTZ02",
    "CWTZ03",
    "CWTZ04",
    "CWTZ05",
    "CWTZ06",
    "CWTZ07",
    "CWTZ08",
    "ANVILTEMPZ01",
    "ANVILTEMPZ02",
    "ANVILTEMPZ03",
    "ANVILTEMPZ04",
    "ANVILTEMPZ05",
    "ANVILTEMPZ06",
    "ANVILTEMPZ07",
    "ANVILTEMPZ08",
    "POSWZ01",
    "POSWZ02",
    "POSWZ03",
    "POSWZ04",
    "POSWZ05",
    "POSWZ06",
    "POSWZ07",
    "POSWZ08",
    "PRESWZ01",
    "PRESWZ02",
    "PRESWZ03",
    "PRESWZ04",
    "PRESWZ05",
    "PRESWZ06",
    "PRESWZ07",
    "PRESWZ08",
    "COOLWZ01",
    "COOLWZ02",
    "COOLWZ03",
    "COOLWZ04",
    "COOLWZ05",
    "COOLWZ06",
    "COOLWZ07",
    "COOLWZ08",
    "ANILTEMPWZ01",
    "ANILTEMPWZ02",
    "ANILTEMPWZ03",
    "ANILTEMPWZ04",
    "ANILTEMPWZ05",
    "ANILTEMPWZ06",
    "ANILTEMPWZ07",
    "ANILTEMPWZ08",
    "ACKKW",
    "ACKKWH",
    "RECORDREF",
    "OPERATORNAME",
    "STIMEMINTOTAL",
    "STIMEHH",
    "STIMEMM",
    "STIMESS",
    "ACKSTEPNO",
    "SERVOPRESSURESSET",
    "SERVOFLOWSET",
    "FRONTPOSITIONSET",
    "REARPOSITIONSET",
    "LEFTPOSITIONSET",
    "RIGHTPOSITIONSET",
    "TOPPOSITIONSET",
    "BOTTOMPOSITIONSET",
    "DOWELSET",
    "ACKTOTTIMEDAYS",
    "ACKTOTALTIMEHH",
    "ACKTOTALTIMEMM",
    "ACKTOTALTIMESS",
    "TOTCOUNTERTIMESS"
]

rm = pyvisa.ResourceManager()
nano_volt = rm.open_resource('GPIB0::7::INSTR')
nano_volt.write('*RST')
nano_volt.write(":SENS:FUNC 'VOLT'; :SENS:CHAN 1;")
sm = rm.open_resource('GPIB0::18::INSTR')

conn, cursor = setup_server()
MODE = 'REVERSE'
csv_filename = f'pressure_resistance-{MODE}-{time.time()}.csv'
headers = ['Timestamp',
           'Load Pressure (bar)', 'Voltage (V)', 'Resistance (ohm)']

epsilon = 1e-9

AVERAGE_COUNT = 5
resistances, voltages, pressures = [], [], []
CURRENT = 500 * 10**-6

def get_current_pressure():
    cursor.execute("SELECT top 1 * FROM [IIT300].[dbo].[ActualLog] WHERE BATCHNO = ? order by id desc",
                   ['HP_CALIB_BIS_CHN_PYRO_A_130325'])
    row = cursor.fetchone()
    if not row:
        return -1
    each_pressure = [
        float(row[MAP.index(f"HYDPRESSURE{i}")]) for i in range(1, 7)]
    return each_pressure


prev_avg_pressure = 0 if MODE == 'FORWARD' else 200

def render():
    global prev_avg_pressure
    # Fetch pressure first
    # Then fetch Voltage
    # Save and plot
    try:
        each_pressure = get_current_pressure()
        if each_pressure == -1:
            return
    except Exception as e:
        print(f"Error fetching pressure: {e}")
        return
    average_pressure = sum(each_pressure)/len(each_pressure)
    if MODE == 'FORWARD':
        if average_pressure < prev_avg_pressure:
            return
    else:
        if average_pressure > prev_avg_pressure:
            return
    avg_volts = [(abs(measure_voltage(-CURRENT)) +
                  abs(measure_voltage(CURRENT))) / 2 for _ in range(AVERAGE_COUNT)]
    avg_volt = sum(avg_volts) / len(avg_volts)
    resistance = avg_volt / (CURRENT + epsilon)

    prev_avg_pressure = average_pressure
    resistances.append(resistance)
    voltages.append(avg_volt)
    pressures.append(average_pressure)

    timestamp = get_time()
    row_data = [timestamp, average_pressure, avg_volt, resistance]
    write_to_csv(csv_filename+".csv", headers, row_data)

    print(f"-----------------------------")
    print(f"Timestamp: {timestamp}")
    print(f"Pressure: {average_pressure} bar")
    print(f"Pressures : ", each_pressure)
    print(f"Avg Voltage: {avg_volt} V")
    print(f"Resistance: {resistance} Ohm")
    print(f"-----------------------------")


plt.style.use('fivethirtyeight')


def animate(i):
    render()
    plt.cla()
    plt.plot(pressures, resistances, c='lightblue',
             linestyle='dashed', zorder=1)
    plt.scatter(pressures, resistances,
                label="Resistance vs Voltage", c='red', zorder=2)
    plt.legend()
    plt.tight_layout()


try:
    plot_animation = FuncAnimation(
        plt.gcf(), animate, interval=1000, cache_frame_data=False)
    plt.show()
finally:
    cursor.close()
    conn.close()
