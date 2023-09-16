import numpy as np
import random
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
from modules_python.config.config import fg, init

def plot(
        data    : dict, 
        legend  : list = None, 
        index   : int=10, 
        channel : int = 1, 
        fig_name: str = "out.png", 
        colors  : list=None,
        type_img: str ='X',
        cmap  : str = 'RdYlBu', 
        save  : bool = False
        ):
    """
    ----------------------------------------------------------

    >>> Copyright : Iréné A. Essomba (c) 2023

    ----------------------------------------------------------

    * data : is a dictionary that contains the images 
    * legend : is a list used for image's titles 
    * index : is an integer used to select a image in data 
    * channel : is an intger belongs to [0, 1, 2] used for colors representation
    * fig_name : is a string used to output and save image
    * colors : is a list used for title's colors
    * type_img : is a string used to select whitch category of images we want to plot it takes two values : ['X', 'images']
    * cmap : is a string for color mapping (2D dimensionnal plot)

    *----------------------------------------------------------------------------------------------------------------------------

    >>> plot(data=data, index = 1, fig_name = "out.png", channel=1, legend=None, colors=None)
    >>> plot(data=data, index = 1, fig_name = "out.png", channel=1, legend=None, colors=['red', 'g', 'm', 'g', 'k'])
    """
    # intialisation de l'incrément 
    idd  = 0

    if data:
        # création d'un canvas de 12 figures 2x6 représentant une espèce unique
        fig, axes = plt.subplots(2, 6, figsize=(12, 4))     
        # verification des coleurs
        if colors is None: colors = random.sample(list(mcolors.CSS4_COLORS.keys()), 12)
        else: pass 
        # definition de la légende
        if legend is None: legend = [f'{x}' for x in range(12)]
        else: pass 

        try:
            if type_img in ['X', 'images']:
                for j in range(6):
                    for i in range(2):
                        X = data[type_img][idd]
                        # conversion dtype(object) ---> dtype(float32)
                        XX = X[index].astype("float")
                        # création de figures avec imshow
                        if type_img == 'X' : axes[i, j].imshow(XX[:, :, channel], cmap=cmap, interpolation="nearest")
                        else : axes[i, j].imshow(XX, interpolation="nearest")
                        # difinir un titre pour chaque plantes 
                        axes[i, j].set_title(legend[idd], fontsize='small', color=colors[idd], weight="bold")
                        # x_axis and y_axis off
                        axes[i, j].axis("off")
                        # incrémentation 
                        idd += 1
                
                # saving figure in .png format 
                if type_img == 'X' : plt.savefig(f"./images/{fig_name}")
                else : plt.savefig(f"./images/{fig_name}") if save is True else ""
                
                plt.show()
            else: 
                error = fg.rbg(255, 0, 255) + " type_img " + fg.rbg(255, 255, 255) + "not in" + fg.rbg(255, 0, 255)+ " ['X', 'images'] " + init.reset
                print(error)
        except IndexError:
            error = fg.rbg(255, 0, 255) + " index " + fg.rbg(255, 255, 255) + "is out of range" + init.reset
            print(error)
    else: 
        error = fg.rbg(255, 0, 255) + " data " + fg.rbg(255, 255, 255) + "cannot be empty" + init.reset
        print(error)