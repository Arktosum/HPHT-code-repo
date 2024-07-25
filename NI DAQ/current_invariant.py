import pyvisa
import time
import datetime

from utils import get_time, write_to_csv

rm = pyvisa.ResourceManager()
nano_volt = rm.open_resource('GPIB0::7::INSTR')
nano_volt.write('*RST')
nano_volt.write(":SENS:FUNC 'VOLT'; :SENS:CHAN 1;")
sm = rm.open_resource('GPIB0::18::INSTR')

resistances = []
pressures = []

def set_current(current):
    sm.write(f":SOUR:CURR {current}")    
    sm.write(f":OUTP ON")

def measure_voltage(current : float):
    current = set_current(current)
    volt = float(nano_volt.query(":READ?"))
    time.sleep(0.01)
    return volt


csv_filename = 'pressure_resistance.csv'
headers = ['Timestamp','Pressure (bar)','Voltage (V)']
epsilon = 1e-9

pressure = 0
while True:
    # pressure = float(input('Enter Pressure (bar) : '))
    avg_volt = 0
    current = 500*10**-6
    for i in range(4):
        min_volt = measure_voltage(-current)
        max_volt = measure_voltage(current)
        volt = (abs(min_volt) + abs(max_volt)) / 2
        avg_volt += volt
        
    avg_volt = avg_volt/4
    resistance = (avg_volt/current)
    resistances.append(resistance)
    pressures.append(pressure)
    
    timestamp = get_time()

    data = [timestamp,pressure,avg_volt,resistance]
    write_to_csv(csv_filename,headers,data)
    print(data)
    pressure+=5
    
