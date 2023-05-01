import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

COLOR = 'w'
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
BACKGROUND = '#36454F'

class GanttChart:
    five_colors = ["#e76f51","#2a9d8f","#e9c46a","#f4a261","#264653"]
    many_colors = ["#001219","#005f73","#0a9396","#94d2bd","#e9d8a6","#ee9b00","#ca6702","#bb3e03","#ae2012","#9b2226"]

    def __init__(self, data: pd.DataFrame, task_col: str = 'task', 
                 start_col: str = 'start_date', end_col: str = 'end_date',
                 complete_col: str = 'percent_completed', 
                 hue_col: str = 'worker'):
        self.data = data
        self.task_col = task_col
        self.start_col = start_col
        self.end_col = end_col
        self.complete_col = complete_col
        self.hue_col = hue_col
        self.data[start_col] = pd.to_datetime(self.data[start_col])
        self.data[end_col] = pd.to_datetime(self.data[end_col])

        start_date = self.data[start_col].min()
        self.start_date = start_date
        self.data['start_num'] = (self.data[start_col] - start_date).dt.days
        self.data['end_num'] = (self.data[end_col] - start_date).dt.days
        self.data['total_days'] = self.data['end_num'] - self.data['start_num']
        if self.data[complete_col].max() > 1:
            self.data[complete_col] /= 100
        self.data['current_num'] = (self.data.total_days * self.data[complete_col])
        self.data.sort_values(by='start_num', inplace=True, ascending=False,
                              ignore_index=True)
        self.fig = None
        self.ax = None
        hues = list(self.data[hue_col].unique())
        colors = self.five_colors
        if len(hues) > 5:
            colors = self.many_colors
        self.colors = {hues[i]: colors[i] for i in range(len(hues))}
        self.data['color'] = self.data.apply(self.color, axis=1)
    
    def color(self, row):
        return self.colors[row[self.hue_col]]

    def plot(self, figsize=(16, 6), minor_steps=7, year=2022):
        self.fig, self.ax = plt.subplots(1, figsize=figsize, tight_layout=True)
        self.ax.barh(self.data[self.task_col], self.data.current_num, 
                     left=self.data.start_num, color=self.data.color)
        self.ax.barh(self.data[self.task_col], self.data.total_days, 
                     left=self.data.start_num, color=self.data.color, alpha=0.5)
        for idx, row in self.data.iterrows():
            self.ax.text(row.end_num+0.1, idx, 
                    f"{int(row[self.complete_col]*100)}%", 
                    va='center', alpha=0.8)
        legend_elements = [Patch(facecolor=self.colors[i], label=i)  for i in self.colors]
        plt.legend(handles=legend_elements, facecolor=BACKGROUND)
        xticks_labels = pd.date_range(self.start_date, 
                end=self.data[self.end_col].max()).strftime("%m/%d")
        xticks = [index for index, date in enumerate(xticks_labels) if "/01" in date]
        xticks_labels = pd.date_range(self.start_date, 
                end=self.data[self.end_col].max()).strftime("%b")
        labels = [xticks_labels[tick] for tick in xticks]
        for i in range(len(labels)):
            if labels[i] == 'Jan':
                labels[i] = str(year)
                year += 1
        xticks_minor = np.arange(0, self.data.end_num.max()+1, minor_steps)
        self.ax.set_xticks(xticks)
        self.ax.set_xticks(xticks_minor, minor=True)
        self.ax.set_xticklabels(labels)
        self.ax.set_title("Gantt Chart")
        self.ax.set_axisbelow(True)
        self.ax.xaxis.grid(color='w', linestyle='dashed', alpha=0.4, which='major')

        self.fig.set_facecolor(BACKGROUND)
        self.ax.set_facecolor(BACKGROUND)

