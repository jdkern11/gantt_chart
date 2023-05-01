import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt

from gantt_chart import GanttChart

df = pd.read_csv('gantt_data.csv')

chart = GanttChart(df)
chart.plot(minor_steps=1)
# chart.fig.show()
# tk.mainloop()
chart.fig.savefig('gantt.png', facecolor=chart.fig.get_facecolor(), 
         edgecolor='none')
