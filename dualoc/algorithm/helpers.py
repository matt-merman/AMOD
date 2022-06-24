from matplotlib import pyplot as mp

grid_color = "grey"
label_color = "white"
plot_color="green"
title_fontsize = 30
axes_fontsize = 20
text_pad = 20
context = {'axes.edgecolor':'grey', 'axes.facecolor':'black',
           'font.family':'monospace', 'figure.facecolor':'black', 'figure.edgecolor':'black',
           'xtick.color':'white', 'ytick.color':'white'}

def showGraph(x_1, y_1, x_2, y_2):
    with mp.rc_context(context):

        mp.figure(figsize=(10,10))
        mp.scatter(x_1, y_1, alpha=0.9, color = 'green', label='Customers')
        mp.scatter(x_2, y_2, alpha=0.9, color = 'red', label='Facilities')
        
        mp.grid(color=grid_color)
        
        mp.title("Geographical Distribution", color=label_color, pad=text_pad, fontsize=title_fontsize)
        mp.legend(fontsize=18, labelcolor=label_color)
        mp.savefig('test.png')
        mp.show()
