import numpy as np
import matplotlib.pyplot as plt
from performance.helpers import *

class Chart:
    def __init__(self):
        self.color = "black"
        self.title_fontsize = 'xx-large'
        self.axes_fontsize = 'x-large'
        self.legend_fontsize = 'large'
        self.text_pad = 70
        self.context = {'axes.edgecolor': 'black', 'axes.facecolor': 'white',
                        'font.family': 'monospace', 'figure.facecolor': 'white',
                        'figure.edgecolor': 'white', 'xtick.color': 'black',
                        'ytick.color': 'black'}
        self.ind = np.arange(3)  # the x locations for the groups
        self.width = 0.25      # the width of the bars
        self.color_list = ['b', 'g', 'r', 'c', 'm', 'y']

    def autolabel(self, rects, ax):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., h, "%.3f" % h,
                    ha='center', va='bottom', rotation=0, fontsize='large', color=self.color)

    def set_chart(self, plt):
        fig = plt.figure(figsize=(10, 7))
        plt.grid(alpha=.3, color=self.color)
        ax = fig.add_subplot(111)
        ax.set_xticklabels(
            ('Dualoc', 'LP_relaxation', 'LP_lagrangian'), fontsize=self.axes_fontsize)
        return ax

    def set_legend(self, ax, plt, rect, facilities, customers):
        l = len(facilities)
        a = tuple((rect[i],) for i in range(0, l))
        n = tuple((facilities[i], customers[i]) for i in range(0, l))

        legend = ax.legend(a, n, title='(facilities, customers)', loc='upper center',
                           bbox_to_anchor=(0.5, 1.15), ncol=3, fontsize=self.legend_fontsize, labelcolor=self.color)
        plt.setp(legend.get_title(), color=self.color,
                 fontsize=self.axes_fontsize)

    def error_chart(self, path, path_to_save):

        value, facilities, customers = create_list(path, 'error')
        l = len(facilities)

        plt_instance = plt

        with plt_instance.rc_context(self.context):

            ax = self.set_chart(plt_instance)

            rect = [[] for _ in range(0, l)]

            for i in range(0, l):
                rect[i] = ax.bar(
                    self.ind + (i * self.width), value[i], self.width, alpha=.5, color=self.color_list[i])
                self.autolabel(rect[i], ax)

            self.set_legend(ax, plt_instance, rect, facilities, customers)

            plt_instance.ylabel('Percentage Error w.r.t. Primal Simplex Solution',
                                fontsize=self.axes_fontsize, color=self.color)

            ax.grid(axis='x')
            ax.set_xticks(self.ind+((l-1)/2)*self.width)
            plt_instance.savefig(path_to_save)
            #plt_instance.show()

    def time_chart(self, path, path_to_save):

        value, facilities, customers = create_list(path, 'time')
        l = len(facilities)

        plt_instance = plt

        with plt_instance.rc_context(self.context):

            ax = self.set_chart(plt_instance)

            rect = [[] for _ in range(0, l)]

            for i in range(0, l):
                rect[i] = ax.bar(
                    self.ind + (i * self.width), value[i], self.width, alpha=.5, color=self.color_list[i])
                self.autolabel(rect[i], ax)

            self.set_legend(ax, plt_instance, rect, facilities, customers)

            plt_instance.ylabel('Execution Time [ms]', fontsize=self.axes_fontsize,
                                color=self.color)

            ax.grid(axis='x')
            ax.set_xticks(self.ind+((l-1)/2)*self.width)
            plt_instance.savefig(path_to_save)
            #plt_instance.show()
