import numpy as np
import random
import matplotlib.pyplot as plt 
from modules_python.config.config import fg, init
from modules_python.image_processing.preprocessing import get_mask, change_bg, erorsion_and_dilation

def SemanticImage(
        data        : dict, 
        index       : int   = 10, 
        channel     : int   = 1, 
        threshold   : list  = [-50, -9.], 
        upper_color : list  = [30, 30, 30], 
        lower_color : list  = [0,0,0],
        legend      : list  = None,
        radius      : int   = 2,
        method      : str   = "numpy",
        bg          : str   = "white", 
        id_sel      : list  = [6, 7, 8, 9, 10, 11],
        deep_mask   : bool  = False,
        kernel      : tuple = (2, 2)
        ):
    
    """
    ----------------------------------------------------------

    >>> Copyright : Iréné A. Essomba (c) 2023

    ----------------------------------------------------------

    The Semantic image  is a powerfull tool used to create a mask for each objects loacted in th image .

    * data : is a dictionary that contains the images 
    * threshold if a list of values of 2 dimension used to delimite the border of the image, threshold = [m1, m2] with m1 < m2
    * radius is a positive float number
    * channel is a channel value and should lower than c
    * method is string value that takes 2 values : numpy and where is the type of calculation
    * upper_color is the maximal channel color and should hace (c, ) dimension 
    * lower_color is the maximal channel color and should hace (c, ) dimension
    * bg = "both", "black" , "white" or "mask"
    * index : is an integer type used to select à particular image
    * legend is a list used for title images
    * kernel : is a tuple used to create a deep mask 
    * deep_mask : is a boolean value used to specify is deep mask should be apply
    * id_sel : is a list of species
    *-----------------------------------------------------------------------------
    
    """

    idd, error = 0, None

    # select speces
    if id_sel:  
        if len(id_sel) == 6: pass 
        else: error = fg.rbg(255, 0, 255) + " len(id_sel) " + fg.rbg(255, 255, 255) + "!=" + fg.rbg(255, 0, 0) + " 6 " + init.reset
    else: id_sel = [6, 7, 8, 9, 10, 11]

    if error is None:
        # checking if legend exists
        if legend : pass 
        else: legend = id_sel.copy()

        if bg in ["white", "black", "mask"] : 
            fig, axes = plt.subplots(1, 6, figsize=(12, 4)) 

            for j in id_sel:
                X           = data['X'][j][index].astype("float32").copy()
                mask        = get_mask(img=X[:, :, channel], threshold=threshold, radius=radius, method=method)
                mask        = mask * 1.0 
                img         = data['images'][j][index].astype("float32").copy()
                shape       = img.shape

                if deep_mask is True : mask      = erorsion_and_dilation(mask, shape=kernel)
                else: pass
            
                img[:, :, 0] = img[:, :, 0] * mask * 1.
                img[:, :, 1] = img[:, :, 1] * mask * 1.
                img[:, :, 2] = img[:, :, 2] * mask * 1.

                new_img = img.reshape((1, shape[0], shape[1], 3))
                new_img = change_bg(imgs=new_img, lower_color=lower_color, upper_color=upper_color)

                if bg == 'white': 
                    for i in range(1):   
                        axes[idd].imshow(new_img[0])
                        axes[idd].set_title(legend[j], fontsize="small")
                        axes[idd].axis("off")
                
                if bg == 'black': 
                    for i in range(1): 
                        axes[idd].axis("off")  
                        axes[idd].imshow(img)
                        axes[idd].set_title(legend[j], fontsize="small")

                if bg == "mask":
                    for i in range(1): 
                        axes[idd].axis("off")  
                        axes[idd].imshow(mask)
                        axes[idd].set_title(legend[j], fontsize="small")

                idd += 1
            plt.show()
        else : 
            error = fg.rbg(255, 0, 255) + " bg " + fg.rbg(255, 255, 255) + "not in" + fg.rbg(255, 0, 0) + " ['white', 'black'] " + init.reset
            print(error)
    else:  print(error)