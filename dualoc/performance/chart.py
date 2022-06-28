import numpy as np
import matplotlib.pyplot as plt
from performance.helpers import *

class Chart:
    def __init__(self):
        self.color = "grey"
        self.title_fontsize = 30
        self.axes_fontsize = 20
        self.text_pad = 20
        self.context = {'axes.edgecolor':'grey', 'axes.facecolor':'black',
                        'font.family':'monospace', 'figure.facecolor':'black', 
                        'figure.edgecolor':'black', 'xtick.color':'grey', 
                        'ytick.color':'grey'}
 
    def create(self, path, attribute): 

        value, trial = create_list(path, attribute)
        
        COLOR = ['b', 'g', 'r', 'c', 'm', 'y']
        N = 3
        ind = np.arange(N)  # the x locations for the groups
        width = 0.10       # the width of the bars
        l = len(trial)

        with plt.rc_context(self.context):

            fig = plt.figure(figsize=(16,7))
            self.ax = fig.add_subplot(111)

            rect = [[] for _ in range(0, l)]
            
            for i in range(0, l):
                rect[i] = self.ax.bar(ind + (i * width), value[i], width, alpha=.5, color=COLOR[i])
                self.autolabel(rect[i])

            plt.grid(alpha=.3, color=self.color)
            plt.title("Mean Values", color=self.color, pad=self.text_pad, fontsize=self.title_fontsize)
            
            a = tuple((rect[i],) for i in range(0, l))
            n = tuple((trial[i]) for i in range(0, l))
            
            legend = self.ax.legend(a, n, title='Number of Trial', fontsize=self.axes_fontsize, labelcolor=self.color)
            plt.setp(legend.get_title(), color=self.color, fontsize=self.axes_fontsize)

            self.ax.set_xticks(ind+((l-1)/2)*width)
            self.ax.set_xticklabels( ('Dualoc', 'LP_relaxation', 'LP_lagrangian'), fontsize=self.axes_fontsize)
            plt.savefig('test.png')
            plt.show()

    def autolabel(self, rects):
        for rect in rects:
            h = rect.get_height()
            self.ax.text(rect.get_x()+rect.get_width()/2., h, '%d'%int(h),
                    ha='center', va='bottom', color=self.color)
