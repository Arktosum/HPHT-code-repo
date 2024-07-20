import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime

rm = pyvisa.ResourceManager()
nano_volt = rm.open_resource('GPIB0::7::INSTR')
nano_volt.write('*RST')
nano_volt.write(":SENS:FUNC 'VOLT'; :SENS:CHAN 1;")

sm = rm.open_resource('GPIB0::18::INSTR')

# sm.write('*RST')
# sm.write(":SOUR:FUNC 'CURR';")

def set_current(current):
    sm.write(f":SOUR:CURR {current}")
    sm.write(f":OUTP ON")

def measure_voltage(current : float):
    current = set_current(current)
    volt = float(nano_volt.query(":READ?"))
    return volt

MIN_RANGE = -200*10**-6
MAX_RANGE = 200*10**-6

STEP = 10
step_size = (MAX_RANGE - MIN_RANGE)/ STEP
this_current= MIN_RANGE
currents = []
voltages = []
resistances = []

csv_filename = 'current_voltage.csv'
headers = ['Timestamp','Current (A)','Voltage (V)',"Resistance (Ohms)"]

def write_to_csv(file_name,headers,row):
    with open(file_name, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        if csv_file.tell() == 0:
            csv_writer.writerow(headers)
        csv_writer.writerow(row)
        
epsilon = 1e-9
plt.figure(figsize=(16,9));

while this_current <= MAX_RANGE:
    avg_volt = 0
    for i in range(5):
        volt = measure_voltage(this_current)
        avg_volt+=volt
    
    avg_volt = volt/5
    resistance = avg_volt/(this_current + epsilon)
    print(f"{this_current} | {avg_volt} | {resistance}")
    currents.append(this_current)
    voltages.append(avg_volt)
    resistances.append(resistance)

    time.sleep(1)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_to_csv(csv_filename,headers,[timestamp,this_current,avg_volt,resistance])
    plt.grid(True)
    plt.plot(currents,resistances)
    plt.pause(0.05)

    this_current += step_size
plt.show()