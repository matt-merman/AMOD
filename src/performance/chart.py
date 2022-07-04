import numpy as np
import matplotlib.pyplot as plt
from performance.helpers import *

COLOR = ['b', 'g', 'r', 'c', 'm', 'y']


class Chart:
    def __init__(self):
        self.color = "grey"
        self.title_fontsize = 15
        self.axes_fontsize = 9
        self.text_pad = 25
        self.context = {'axes.edgecolor': 'grey', 'axes.facecolor': 'black',
                        'font.family': 'monospace', 'figure.facecolor': 'black',
                        'figure.edgecolor': 'black', 'xtick.color': 'grey',
                        'ytick.color': 'grey'}
        self.ind = np.arange(3)  # the x locations for the groups
        self.width = 0.10       # the width of the bars

    def autolabel(self, rects, ax):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., h, "%.4f" % h,
                    ha='center', va='bottom', rotation=0, fontsize='xx-small', color=self.color)

    def set_chart(self, plt):
        fig = plt.figure(figsize=(16, 7))
        plt.grid(alpha=.3, color=self.color)
        ax = fig.add_subplot(111)
        ax.set_xticklabels(
            ('Dualoc', 'LP_relaxation', 'LP_lagrangian'), fontsize=self.axes_fontsize)
        return ax

    def set_legend(self, ax, plt, rect, trial):
        l = len(trial)
        a = tuple((rect[i],) for i in range(0, l))
        n = tuple((trial[i]) for i in range(0, l))

        legend = ax.legend(a, n, title='Number of Trial', loc='upper center', markerscale=.85,
                           bbox_to_anchor=(0.5, 1.05), ncol=6, fontsize=self.axes_fontsize, labelcolor=self.color)
        plt.setp(legend.get_title(), color=self.color,
                 fontsize=self.axes_fontsize)

    def error_chart(self, path):

        value, trial = create_list(path, 'error')
        l = len(trial)

        plt_instance = plt

        with plt_instance.rc_context(self.context):

            ax = self.set_chart(plt_instance)

            rect = [[] for _ in range(0, l)]

            for i in range(0, l):
                rect[i] = ax.bar(
                    self.ind + (i * self.width), value[i], self.width, alpha=.5, color=COLOR[i])
                self.autolabel(rect[i], ax)

            plt_instance.title("Percentage Error w.r.t. Primal Simplex Solution",
                               color=self.color, pad=self.text_pad, fontsize=self.title_fontsize)

            self.set_legend(ax, plt_instance, rect, trial)

            plt_instance.ylabel('Percentage Error (%)',
                                fontsize=self.axes_fontsize, color=self.color)

            ax.set_xticks(self.ind+((l-1)/2)*self.width)
            plt_instance.savefig('./performance/result/result_error.png')
            plt_instance.show()

    def time_chart(self, path):

        value, trial = create_list(path, 'time')
        l = len(trial)

        plt_instance = plt

        with plt_instance.rc_context(self.context):

            ax = self.set_chart(plt_instance)

            rect = [[] for _ in range(0, l)]

            for i in range(0, l):
                rect[i] = ax.bar(
                    self.ind + (i * self.width), value[i], self.width, alpha=.5, color=COLOR[i])
                self.autolabel(rect[i], ax)

            plt_instance.title("Average Time of Execution", color=self.color,
                               pad=self.text_pad, fontsize=self.title_fontsize)

            self.set_legend(ax, plt_instance, rect, trial)

            plt_instance.ylabel('Time (s)', fontsize=self.axes_fontsize,
                                color=self.color)

            ax.set_xticks(self.ind+((l-1)/2)*self.width)
            plt_instance.savefig('./performance/result/result_time.png')
            plt_instance.show()
