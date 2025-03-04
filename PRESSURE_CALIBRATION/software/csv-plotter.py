import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import filedialog, ttk

def load_csv():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Remove extra spaces
        if df.shape[1] >= 2:  # Ensure at least two columns exist
            x_column.set(df.columns[0])
            y_column.set(df.columns[1])
            update_plot()

def update_plot():
    global df  # Ensure we use the updated DataFrame

    # Clear previous plot
    ax.clear()
    
    if not x_column.get() or not y_column.get():
        return

    x_data = df[x_column.get()]
    y_data = df[y_column.get()]

    # Plot x vs y
    if plot_type.get() == "Line":
        ax.plot(x_data, y_data, marker='o', label=f"{x_column.get()} vs {y_column.get()}")
    else:
        ax.scatter(x_data, y_data, label=f"{x_column.get()} vs {y_column.get()}")
    
    ax.set_xlabel(x_column.get())
    ax.set_ylabel(y_column.get())
    ax.set_title("CSV Data Plot")
    ax.grid(True)  # Enable grid
    ax.legend(loc='upper left')
    
    canvas.draw()

# GUI Setup
root = tk.Tk()
root.title("CSV Plotter")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Load CSV", command=load_csv).pack(side=tk.LEFT, padx=5)
plot_type = tk.StringVar(value="Line")

ttk.Combobox(frame, textvariable=plot_type, values=["Line", "Scatter"])\
    .pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Plot", command=update_plot).pack(side=tk.LEFT, padx=5)

x_column = tk.StringVar()
y_column = tk.StringVar()
df = pd.DataFrame()

# Create a frame to contain the toolbar and canvas
plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

# Matplotlib Figure
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.draw()

# Pack the canvas and toolbar into the frame
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
toolbar = NavigationToolbar2Tk(canvas, plot_frame)
toolbar.update()
toolbar.pack(side=tk.TOP, fill=tk.X)

root.mainloop()
