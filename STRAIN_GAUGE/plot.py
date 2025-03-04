import random

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

df = pd.read_csv('serial_data.csv')

def animate(i):
    time = df.iloc[:, 0]
    raw_analog_value = df.iloc[:, 1]
    average_value = df.iloc[:, 2]
    voltage = df.iloc[:, 3]
    
    plt.cla()
    plt.plot(time, raw_analog_value,label='Raw analog value')
    plt.plot(time, average_value,label='Average value')
    plt.plot(time, voltage,label='Voltage')

    plt.legend(loc='upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(),animate,1000)

plt.show()
