import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
from utils import get_time, write_to_csv
from matplotlib.animation import FuncAnimation

rm = pyvisa.ResourceManager()
nano_volt = rm.open_resource('GPIB0::7::INSTR')
nano_volt.write('*RST')
nano_volt.write(":SENS:FUNC 'VOLT'; :SENS:CHAN 1;")
sm = rm.open_resource('GPIB0::18::INSTR')

def set_current(current):
    sm.write(f":SOUR:CURR {current}")    
    sm.write(f":OUTP ON")

def measure_voltage(current : float):
    current = set_current(current)
    volt = float(nano_volt.query(":READ?"))
    time.sleep(1)
    return volt

EXP_NO = 1
csv_filename = f'pressure_resistance-{EXP_NO}.csv'
headers = ['Timestamp','Pressure (bar)','Voltage (V)','Resistance (ohms)']
epsilon = 1e-9
AVERAGE_COUNT  = 4
pressure = 0

resistances = []
voltages = []
pressures = []

current = 500*10**-6
def render():
    try:
        pressure = float(input('Enter Pressure (bar) : '))
    except:
        print("Invalid Input, please try again.")
        return
    avg_volts = []
    for i in range(AVERAGE_COUNT):
        min_volt = measure_voltage(-current)
        max_volt = measure_voltage(current)
        volt = (abs(min_volt) + abs(max_volt)) / 2
        avg_volts.append(volt)
        
    avg_volt = sum(avg_volts)/len(avg_volts)
    resistance = (avg_volt/(current+epsilon))
    # ----------------------------
    resistances.append(resistance)
    voltages.append(avg_volt)
    pressures.append(pressure)
    # ----------------------------
    # ----------------------------
    timestamp = get_time()
    data = [timestamp,pressure,avg_volt,resistance]
    write_to_csv(csv_filename,headers,data)
    print(data)
    # ----------------------------

plt.style.use('fivethirtyeight')
time.sleep(0.01)
def animate(i):
    render()
    plt.cla()
    plt.plot(pressures,voltages,c='lightblue',linestyle='dashed',zorder=1)
    plt.scatter(pressures,voltages,label="Pressure vs Voltage",c='red',zorder=2)
    plt.legend()
    plt.tight_layout()
plot_animation = FuncAnimation(plt.gcf(),animate,interval=100,cache_frame_data=False)
plt.show()

