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
print(nano_volt.query("*IDN?"))


def measure_voltage():
    volt = float(nano_volt.query(":READ?"))
    return volt

time.sleep(0.01)
for i in range(10):
    print(measure_voltage())
    time.sleep(0.01)

print("Done Testing!")