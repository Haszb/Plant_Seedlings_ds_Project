import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt

def hist_plot(
        data   : list, 
        legend : list,
        title  : list, 
        xlabel : list,
        ylabel : list,
        box    : list = [(0.5, 0.2, 0.5, 0.5)]
        ):
  

    sns.color_palette()
    fig, axes = plt.subplots(1, len(data), figsize=(5 * len(data), 3), squeeze=True, sharey=True)

    for i in range(len(data)):
        axes[i].hist(data[i], bins=10, histtype='bar')
        axes[i].set_title(title[i], weight="bold")
        axes[i].set_xlabel(xlabel[i],  weight="bold")
        axes[i].set_ylabel(ylabel[i],  weight="bold")
        axes[i].legend(legend, bbox_to_anchor=box[i])

    plt.show()

    return [ax for ax in axes]

def annotate(
        axes    : list,
        text    : list = ["bonding box"], 
        color   : str = 'k',
        xytext  : list = [(700, 210)],
        xy      : list = [(450, 210)],
        c       : list = ['k']
    ):

    for i, ax in enumerate(axes):
        ax.annotate(text=text[i], xy=xy[i], arrowprops=dict(arrowstyle='->', color=color), xytext=xytext, color=c[i], weight='bold' )
    plt.show()

def text(
        axes : list,
        x    : list = [600],
        y    : list = [180],
        s    : list = ['$range = [100, 400]$'],
        color : str = "k"
    ):

    for i, ax in enumerate(axes):
        ax.text(x=x[i], y=y[i], s=s[i],  weight="bold", color=color)
    plt.show()

def rect_box(
        axes : list,
        x    : list,
        y    : list,
        xmin : list,
        xmax : list, 
        ymin : list,
        ymax : list,
        color : str = 'k'
        ):
    
    for i, ax in enumerate( axes ):
        ax.vlines(x=x[i][0], ymin=ymin[i], ymax=ymax[i], lw=2, colors=color)
        ax.vlines(x=x[i][1], ymin=ymin[i], ymax=ymax[i], lw=2, colors=color)

        ax.hlines(y=y[i][0], xmin=xmin[i], xmax=xmax[i], lw=2, colors=color)
        ax.hlines(y=y[i][1], xmin=xmin[i], xmax=xmax[i], lw=2, colors=color)
    
    plt.show()

def pie():
    pass 