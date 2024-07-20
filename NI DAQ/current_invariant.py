import pyvisa
import time
import matplotlib.pyplot as plt
import csv
import datetime

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
    return volt

def write_to_csv(file_name,headers,row):
    with open(file_name, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        if csv_file.tell() == 0:
            csv_writer.writerow(headers)
        csv_writer.writerow(row)

csv_filename = 'pressure_resistance.csv'
headers = ['Timestamp','Pressure (bar)','Voltage (V)']
epsilon = 1e-9

plt.figure(figsize=(16,9));
while True:
    pressure = float(input('Enter Pressure (bar) : '))
    avg_volt = 0
    current = 500*10**-6
    for i in range(4):
        min_volt = measure_voltage(-current)
        max_volt = measure_voltage(current)
        avg_volt+= (abs(min_volt) + abs(max_volt)) / 2
        
    avg_volt = avg_volt/4    
    resistance = (avg_volt/current)
    resistances.append(resistance)
    pressures.append(pressure)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    time.sleep(1)
    write_to_csv(csv_filename,headers,[timestamp,pressure,avg_volt])
    
    plt.grid(True)
    plt.plot(pressures,resistances)
    plt.pause(0.05)

