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
sm.write('*RST')
sm.write(":SOURce:FUNCtion CURRent")
sm.query(":MEASure:VOLTage?")

print(nano_volt.query("*IDN?"))
print(sm.query("*IDN?"))

def set_current(current):
    sm.write(f":SOUR:CURR {current}")
    sm.write(f":OUTP ON")

def measure_voltage(current : float):
    current = set_current(current)
    volt = float(nano_volt.query(":READ?"))
    time.sleep(0.01)
    return volt


MIN_RANGE = -500*10**-6
MAX_RANGE = 500*10**-6
STEP = 10 
step_size = (MAX_RANGE - MIN_RANGE)/ STEP
current = MIN_RANGE

currents = []
voltages = []
resistances = []

AVERAGE_COUNT  = 5
EXP_NO = 1
epsilon = 1e-9

csv_filename = f'iv_at_187_bar.csv'
headers = ['Timestamp','Current (A)','Voltage (V)',"Resistance (Ohms)"]

def render():
    global current
    if current > MAX_RANGE:
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
    data = [timestamp,current,avg_volt,resistance]
    write_to_csv(csv_filename,headers,data)
    print(data)
    current += step_size
    # ---------------------------------
    

plt.style.use('fivethirtyeight')
time.sleep(0.01)
def animate(i):
    render()
    plt.cla()
    plt.plot(currents,voltages,c='lightblue',linestyle='dashed',zorder=1)
    plt.scatter(currents,voltages,label="Current vs Voltage",c='red',zorder=2)
    plt.legend()
    plt.tight_layout()
    
plot_animation = FuncAnimation(plt.gcf(),animate,interval=100,cache_frame_data=False)
plt.show()


    
    
    

    
