import numpy as np
import seaborn as sns 
import random
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

def hist_hist_plot(
        X       : list, 
        legend  : list,
        title   : list  = ['', ''], 
        xlabel  : list  = ['', ''],
        ylabel  : list  = ["", ""],
        box     : list  = [(0.5, 0.2, 0.5, 0.5), (0.5, 0.2, 0.5, 0.5)], 
        colors  : list  = [],
        figsize : tuple = None, 
        style   : int   = None,
        y_lim   : list  = [-5, 250],
        bins    : int   = 10,
        grille  : bool  = False, 
        bonding_box : bool = False,
        coord   : dict = {"x" : [[10, 250], [10, 250]], 
                        "y" : [[0, 245], [0, 245]], "xmin":[0, 0], "ymin":[0, 0],
                        "xmax" : [250, 250], "ymax" :  [245, 245]},
        annot   : bool = False, 
        text    : bool = False,
        s       : list = ['$range = [90, 250]$', '$range = [90, 250]$'],
        Types   : list = ["hist", "hist"]
        ):
    
    error = None 

    if bonding_box is True:
        x       = coord['x']
        y       = coord['y']
        xmin    = coord['xmin']
        xmax    = coord['xmax']
        ymin    = coord['ymin']
        ymax    = coord['ymax']
    else: pass 

    if grille is True : plt.grid()
    if style is not None : 
        av = list(plt.style.available)
        if style >= len(av) : pass 
        else: plt.style.use(av[style])
    if figsize is None: figsize = (10, 3)
    if colors: pass 
    else: colors = random.sample(list(mcolors.CSS4_COLORS.keys()), len(legend))

    sns.color_palette()
    fig, axes = plt.subplots(1, 2, figsize=figsize, squeeze=True, sharey=True)

    for i in range(len(X)):
        if Types[i] == 'hist':
            axes[i].hist(X[i], bins=bins, histtype='bar', color = colors)
            axes[i].set_title(title[i], weight="bold")
            axes[i].set_xlabel(xlabel[i],  weight="bold")
            axes[i].set_ylabel(ylabel[i],  weight="bold")
            axes[i].legend(legend, bbox_to_anchor=box[i])
            axes[i].set_ylim(y_lim)
        else:
            error = True 
            break

    if error is None:
        if bonding_box is True: 
            rect_box(axes=axes, x=x, y=y, xmin=xmin, xmax=xmax, 
                     ymin=ymin, ymax=ymax, text=text, annot=annot,s=s)
        else: pass

        plt.show()

        return [ax for ax in axes]
    else:
        print("ERROR")
        for i in range(len(X)):
            axes[i].remove()  
        return None

def hist_bar_plot(
        X       : list, 
        figsize : tuple = (12, 3), 
        Types   : list  = ["hist", "bar"], 
        colors  : list  = None, 
        box     : tuple = (0.5, 0.1, 0.5, 0.5),
        legend  : list  = [],
        bb_box  : dict  = {"x":1500, "y":250},
        s       : str   = '$range = [50, 250]$\n$pixel=\dfrac{largeur * hauteur}{1024}$',
        rot     : float = 10,
        titles  : list  = ["Histograme de Pixelisation", "Nombre de plantes par espèce"],
        xlabel  : list  = ['', ''],
        ylabel  : list  = ['', ''],
        y_lim   : list  = [[-5, 330], [-5, 720]],
        style   : int   = None,
        grille  : bool  = False,
        c       : str   = 'k',
        ls      : str   = '--',
        lw      : float = 2.,
        width   : float = 0.3,
        bins    : int   = 10,
        legends : list  = None,
        gama    : list  = None 
        ):

    if grille is True : plt.grid()
    if style is not None : 
        av = list(plt.style.available)
        if style >= len(av) : pass 
        else: plt.style.use(av[style])
    if figsize is None: figsize = (10, 3)
    if colors: pass 
    else: colors = random.sample(list(mcolors.CSS4_COLORS.keys()), len(legend))

    sns.color_palette()

    fig, axes = plt.subplots(1, len(X), figsize=figsize, squeeze=True)

    for i in range(len(X)):
        if Types[i] == "hist":
            axes[i].hist(X[i], bins=bins, color=colors )
            axes[i].legend(legend, bbox_to_anchor=box)
            axes[i].text(x=bb_box['x'], y=bb_box['y'], s=s)

        elif Types[i] == "bar":
            if legends is None: pass 
            else:
                legend = legends
                colors  = colors + list( random.sample(list(mcolors.CSS4_COLORS.keys()), 6 ) )
                X[i]    = gama

            axes[i].bar(x=range(len(legend)), height=X[i], color=colors, width=width)
            axes[i].scatter(x=range(len(legend)), y=X[i], s=30, color="w")
            axes[i].plot(X[i], color=c, ls = ls, lw=lw)
            axes[i].set_xticks(range(len(legend)), legend, rotation=rot, ha="center")

        axes[i].set_ylim(y_lim[i])
        axes[i].set_xlabel(xlabel[i],  weight="bold")
        axes[i].set_ylabel(ylabel[i],  weight="bold")
        axes[i].set_title(titles[i],  weight="bold")
        

    plt.show() 

def hist_pie_plot(
        X       : list, 
        figsize : tuple = (12, 3), 
        Types   : list  = ["hist", "pie"], 
        colors  : list  = None, 
        box     : tuple = (0.5, 0.1, 0.5, 0.5),
        legend  : list  = [],
        bb_box  : dict  = {"x":1.5, "y":250},
        s       : str   = '$range = [0.92, 1.3]$\n$frac=\dfrac{ largeur }{ hauteur} \sim 1$',
        titles  : list  = ["Variation de largeur\hauteur", ""],
        xlabel  : list  = ['', ''],
        ylabel  : list  = ['', ''],
        y_lim   : list  = [-5, 330],
        style   : int   = None,
        grille  : bool  = False,
        bins    : int   = 10,
        vline   : bool  = False,
        vh_lw   : float = 2.0, 
        radius  : float = 0.75,
        pctdistance : float = 0.85,
        x_lim   : list  = [0.95, 1.2],
        v_line  : float = 1.005, 
        Sobel_legends : list = None
        ):

    if grille is True : plt.grid()
    if style is not None : 
        av = list(plt.style.available)
        if style >= len(av) : pass 
        else: plt.style.use(av[style])
    if figsize is None: figsize = (10, 3)
    if colors: pass 
    else: colors = random.sample(list(mcolors.CSS4_COLORS.keys()), len(legend))

    sns.color_palette()
    sum_ = sum(X[1])
    if sum_ != 0 : 
        N = len(X)
        fig, axes = plt.subplots(1, len(X), figsize=figsize, squeeze=True)
    else: 
        N = 1
        fig, axes = plt.subplots(1, 1, figsize=figsize, squeeze=True)

    if N > 1:
        for i in range(N):
            if Types[i] == "hist":
                axes[i].hist(X[i], bins=bins, color=colors )
                axes[i].legend(legend, bbox_to_anchor=box)
                axes[i].text(x=bb_box['x'], y=bb_box['y'], s=s)
                if vline is True:
                    axes[i].vlines(x=v_line, ymax=y_lim[1], ymin=y_lim[0], lw = vh_lw, colors="k")
                
                axes[i].set_xlabel(xlabel[i],  weight="bold")
                axes[i].set_ylabel(ylabel[i],  weight="bold")
                axes[i].set_title(titles[i],  weight="bold")
                axes[i].set_ylim(y_lim)
                axes[i].set_xlim(x_lim)
            elif Types[i] == "pie":
                axes[i].pie(x=list(X[i]),
                    textprops=dict(c="black", weight="bold"), 
                    autopct=lambda pct : auto_pct(pct, X[i]), 
                    pctdistance=pctdistance, colors=colors)
                center_circle = plt.Circle((0, 0), radius=radius, fc='white')
                plt.gca().add_artist(center_circle)
                axes[i].set_title(f"Canaux RGBA = ${[int(x) for x in X[i]]}$",  weight="bold")
                axes[i].legend(Sobel_legends, fontsize='x-small', bbox_to_anchor=(0.23, 0.32, 0.5, 0.4), title="Plant's Names")
    else:
        i = 0
        axes.hist(X[i], bins=bins, color=colors )
        axes.legend(legend, bbox_to_anchor=box)
        axes.text(x=bb_box['x'], y=bb_box['y'], s=s)
        if vline is True:
            axes.vlines(x=v_line, ymax=y_lim[1], ymin=y_lim[0], lw = vh_lw, colors="k")
        
        axes.set_xlabel(xlabel[i],  weight="bold")
        axes.set_ylabel(ylabel[i],  weight="bold")
        axes.set_title(titles[i],  weight="bold")
        axes.set_ylim(y_lim)

    plt.show()
            
def auto_pct(pct, dataset):
    value = int(round(pct / np.sum(dataset)) * 100.0 )
    return "{0:0.0f}%".format(pct, value)
        
def rect_box(
        axes    : list,
        x       : list,
        y       : list,
        xmin    : list,
        xmax    : list, 
        ymin    : list,
        ymax    : list,
        color   : str  = 'k',
        s       : list = ['$range = [90, 250]$', '$range = [90, 250]$'],
        text    : bool = False ,
        annot   : bool = False
        ):
    
    for i, ax in enumerate( axes ):
        ax.vlines(x=x[i][0], ymin=ymin[i], ymax=ymax[i], lw=2, colors=color)
        ax.vlines(x=x[i][1], ymin=ymin[i], ymax=ymax[i], lw=2, colors=color)

        ax.hlines(y=y[i][0], xmin=xmin[i], xmax=xmax[i], lw=2, colors=color)
        ax.hlines(y=y[i][1], xmin=xmin[i], xmax=xmax[i], lw=2, colors=color)

        if text is True:
            ax.text(x=xmax[i]+100, y=ymax[i]-70, s = s[i] )
        if annot is True:
            ax.annotate(text="bonding box", xy=(xmax[i], ymax[i]-40), arrowprops=dict(arrowstyle='->', color="k"), 
                     xytext=(xmax[i] + 150, ymax[i]-40), color="b", weight='bold' )
    
    plt.show() 