import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./serial_data.csv',header=None)
plt.plot([i for i in range(len(df))],df[3])

print("Max strain : ",max(df[3]))
plt.grid(True)
plt.show()