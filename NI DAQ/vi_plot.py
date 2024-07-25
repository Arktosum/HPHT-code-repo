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


MIN_RANGE = -200*10**-6
MAX_RANGE = 200*10**-6

STEP = 5
step_size = (MAX_RANGE - MIN_RANGE)/ STEP
this_current= MIN_RANGE
currents = []
voltages = []
resistances = []

AVERAGE_COUNT  = 5
EXP_NO = 1
csv_filename = f'current_voltage-{EXP_NO}.csv'
headers = ['Timestamp','Current (A)','Voltage (V)',"Resistance (Ohms)"]

plt.style.use('fivethirtyeight')
plt.get_current_fig_manager().window.showMaximized()

epsilon = 1e-9
time.sleep(0.01)
def animate(i):
    global this_current
    if this_current > MAX_RANGE:
        return
        
    # Measure AVERAGE_COUNT volts and take average
    avg_volts = []
    for i in range(AVERAGE_COUNT):
        volt = measure_voltage(this_current)
        avg_volts.append(volt)
        
    # calculate average voltage
    avg_volt = sum(avg_volts)/len(avg_volts)
    
    # Calculate Resistance  R = V/I
    resistance = avg_volt/(this_current + epsilon)
    
    
    currents.append(this_current)
    voltages.append(avg_volt)
    resistances.append(resistance)

    timestamp = get_time()
    data = [timestamp,this_current,avg_volt,resistance]
    write_to_csv(csv_filename,headers,data)
    print(data)
    this_current += step_size
    
    
    plt.cla()
    plt.plot(currents,voltages,label="Current vs Voltage")
    plt.legend()
    plt.tight_layout()
    
plot_animation = FuncAnimation(plt.gcf(),animate,interval=100)


plt.show()


    
    
    

    
