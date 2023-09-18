##########################################################################################
##########################################################################################
from skimage.color.adapt_rgb import each_channel, hsv_value, adapt_rgb                   #
from skimage.exposure import equalize_hist, equalize_adapthist, rescale_intensity        #
from skimage import transform, filters                                                   #
from skimage.color import rgb2gray, rgba2rgb                                             #
from skimage.morphology import disk                                                      #
from skimage.util import img_as_ubyte                                                    #
import numpy as np                                                                       #
import cv2                                                                               #
from skimage.morphology import closing, opening                                          #
from modules_python.config.config  import init, fg, bg                                                          #
##########################################################################################
# Copyright : Iréné A. Essomba (c) 2023                                                  #
##########################################################################################

@adapt_rgb( each_channel )
def sobel_each( imgage )        :
    # sobel channel
    img = filters.sobel( imgage )
    return img

@adapt_rgb( hsv_value )
def sobel_hsv( image )          :
    # histogram value 
    img = filters.sobel( image )
    return img

def simple_gray( image )        :
    # channel n to 1
    return  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def GaussionBlur(image)         :
    # Gaussian Blur (GB)
    img = simple_gray(image)
    return cv2.GaussianBlur(src=img, ksize=(0,0), sigmaX=3)

def histogram( image, typ : str = "contrast" )  :
    # Contrast Stretching (CS)
    if typ =="contrast":
        p2, p98 = np.percentile(image, (2, 98))
        img_scale = rescale_intensity(image, in_range=(p2, p98))
        return img_scale

    #Grayscale / Histogram Equalization (HE)
    elif typ == "equal":
        img = simple_gray(image)
        img_equal = equalize_hist(img)
        return  img_equal 

    # ---- Grayscale / Contrast Limited Adaptive Histogram Equalization (CLAHE)  
    elif typ == "equal_adapt":
        img = simple_gray(image)
        img_adapteq = equalize_adapthist(img)
        return img_adapteq 
    
    #  ---- Grayscale / Local Histogram Equalization (LHE)
    else:
        footprint = disk(10)
        img = simple_gray( image )
        img = img_as_ubyte( img )
        img_eq_disk = filters.rank.equalize(img, footprint=footprint) / 255.0

        return  img_eq_disk 
    
def image_processing( image : np.ndarray, name : str = "RGB", reshape : tuple = (160, 160), add_contrast: bool = False):
    """
    Copyright : Iréné A. Essomba (c) 2023
    
    """
    # forme du maillaage 
    if reshape: width, height = reshape

    imgs            = image.copy()
    sobel           = False 
    filter          = None 

    # Conversion de rbga à rbg (channel = 4 ---> channel = 3)
    if imgs.shape[2] >= 4: 
        imgs    = rgba2rgb ( imgs )
        sobel   = True 

    # redimensionner l'image 
    if reshape is None: pass 
    else : imgs = transform.resize( image = imgs, output_shape=(width, height) )
    
    # rbg to histogram color 
    if   name == "RBG-HSV"      : filter = sobel_hsv( imgs ) 
    # histogram Contrast stretching
    elif name == "HIS-C"        : filter = histogram(imgs, typ = "contrast") 
    # hsitogram equalize 
    elif name == "HIS-EQ"       : filter = histogram(imgs, typ = "equal") 
    # histogram Adaptive Equalization
    elif name == "HIS-ADAPT"    : filter =  histogram(imgs, typ = "equal_adapt") 
    # histogram disk
    elif name == "HIS-DISK"     : filter =  histogram(imgs, typ = "disk") 
    # rgb to gary
    elif name == "SIMPLE_GRAY"  : filter = simple_gray( imgs ) 
    # gaussian blur
    elif name == "GAUSSIAN"     : filter =  GaussionBlur( imgs ) 
    # "RGR2-HVS"
    elif name == "RGR2-HVS"     : filter = cv2.cvtColor(imgs, cv2.COLOR_BGR2HSV)
    # "RGR2-LAB"
    elif name == "RGR2-LAB"     : 
        if add_contrast is False : filter = cv2.cvtColor(imgs, cv2.COLOR_BGR2LAB)
        else : 
            img_    =   histogram(imgs, typ = "contrast") 
            filter  = cv2.cvtColor(img_, cv2.COLOR_BGR2LAB)
    # rbg
    else                        : filter =  imgs

    return filter, sobel

def Size(image : np.ndarray)-> tuple:
    # initialize values
    width, height, channel = image.shape

    # compute the report 
    r       = width / height
    # compute the pixels of image
    pixel   = (width * height ) / 1024

    # returning values 
    return r, pixel

def img_encoding(image : np.ndarray, mask : np.ndarray):
    img = image.copy()

    img[..., 0] = img[..., 0] * mask * 1
    img[..., 1] = img[..., 1] * mask * 1
    img[..., 2] = img[..., 2] * mask * 1

    return img

def Best_mask(img : np.ndarray, mask_1 : np.ndarray, mask_2 : np.ndarray):

    import tensorflow as tf 

    # distnace between encoding and identity
    image_1     = img_encoding(image=img, mask=mask_1)
    image_2     = img_encoding(image=img, mask=mask_2)

    dist1       = tf.reduce_sum( tf.square( tf.subtract(img, image_1) ) ) 
    dist2       = tf.reduce_sum( tf.square( tf.subtract(img, image_2) ) )

    if dist1 < dist2: return (mask_1, "mask1")
    else: return (mask_2, "mask2") 

def get_mask(img : np.ndarray, threshold : list = [10, 50] , radius: float = 2, method : str = 'numpy') -> np.ndarray:

    """
    Copyright : Iréné A. Essomba (c) 2023



    * img is an image of (m, m, c) dimension, c is the channel , (m, m) is the width and height 
    * threshold if a list of values of 2 dimension used to delimite the border of the image, threshold = [m1, m2] with m1 < m2
    * radius is positive float number
    * method is string value that takes 2 values : numpy and where is the type of calculation

    *--------------------------------------------------------------------------------------------------

    >>> img = np.random.randn(160, 160, 3)
    >>> mask = get_mask(img = img, threshold=[10, 50], radius=2, method='numpy')
    >>> mask = get_mask(img = img, threshold=[10, 50], radius=2, method='where')

    """

    from skimage.morphology import closing
    from skimage.morphology import disk  

    # numpy method
    if method == "numpy": filter = ( img > threshold[0]  ) & ( img < threshold[1] ) 
    # where method
    else: filter = np.where( ( img > threshold[0]  ) & ( img < threshold[1] ), 1, 0)

    # create a disk
    S = disk(radius)
    # create filter by comparing the values close to S or inside the disk
    filter = closing(filter, S)

    # returning values
    return filter

def erorsion_and_dilation(img : np.ndarray, show : bool = False, shape=(3,3)) -> np.ndarray:
    """ 
    Copyright : Iréné A. Essomba (c) 2023


    * img is the image with (m, m, c) dimension 
    * show is a bool value initialized on false. used to plot curve 
    * shape is the kernel used to make errosion and dilation. it has (n, n) dimension 

    * -------------------------------------------------------------

    >>> img = np.random.randn(160, 160, 3)
    >>> new_img = errorsion_and_dilation(img = img, shape = (2, 2))

    """

    # module loading
    import matplotlib.pyplot as plt 
    from scipy import ndimage

    x_open = ndimage.binary_opening(img, structure=np.ones(shape))

    if show is True:
        plt.matshow(x_open, interpolation="nearest") 
        plt.axis("off")
        plt.show()
    else: pass

    return x_open

def float_to_int(imgs : np.ndarray, dtype : str = "int32") -> np.ndarray:

    """
    Copyright : Iréné A. Essomba (c) 2023



    * imgs is a ndarray type with (m, m, c) dimension 
    * dtype is the imgs data type 

    creating bins between [0, 255]
    then converting into integer types 

    >>> Examples

    >>> imgs = np.random.randn(100, 160, 160, 3)
    float_to_int(imgs = imgs, dtype = "int32")

    * The default value is int32

    >>>  float_to_int(imgs = imgs)

    """
    # intitializing 
    image       = imgs.copy() 
    dtype_lists = ['int8', 'int32', 'int64', 'int128', 'int256']

    # checking the type of image
    if type(imgs) == type(np.array([0])):
        # checking if we got the right dtype 
        if dtype in dtype_lists:  image = (image * 255).astype(dtype=dtype)
        else: 
            error = init.bold + fg.rbg(0, 255, 0) + f"{dtype}{fg.black_L} not in the list {fg.rbg(255, 75, 50)}{dtype_lists}" + init.reset
            print(error)
    else: 
        t = type(np.array([0]))
        error = init.bold + fg.rbg(0, 255, 0) + f"imgs {fg.white_L} is not {fg.rbg(255,0,0)}{t}" + init.reset
        print(error)
    
    return image

def change_bg(imgs : np.ndarray, upper_color : list, lower_color : list, dtype : str = "int32"):
    """
    Copyright : Iréné A. Essomba (c) 2023



    * imgs is a ndarray type with (n, m, m, c) dimension 
      n is the samples, (m, m, c) the features of image
    * upper_color is the maximal channel color and should hace (c, ) dimension 
    * lower_color is the maximal channel color and should hace (c, ) dimension 
    * dtype is the imgs data type

    to change the background color (BGC) we need to create a mask to fix the border limit 
    where the filter can be applied. To do that we will use the argument

    - upper_color 
    - lower color

    >>> lower_color = np.array([0, 0, 0]) 
    >>> upper_color = np.array([30, 30, 30])
    >>> mask = cv2.inRange(imgs, lower_color, upper_color)
    >>> dtype = ['int8', 'int32', 'int64', 'int128', 'int256']
    * ------------------------------------------------------------

    >>> imgs = np.random.randn(100, 160, 160, 3)
    >>> new_imgs = change_bg(imgs=imgs, upper_color=[30, 30, 30], lower_color=[0, 0, 0], dtype="int32")

    *-------------------------------------------------------------
    >>> new_imgs.shape = imgs.shape = (100, 160, 160, 3)

    """
    if type(imgs) == type(np.array([0])):
        IMGS = imgs.copy()
        shape = IMGS.shape
        if upper_color:
            if len(upper_color) == len(lower_color):
                if len(upper_color) == shape[-1]:
                    upper_color = np.array(upper_color).reshape((shape[-1], ))
                    lower_color = np.array(lower_color).reshape((shape[-1], ))
                    try:
                        prod = upper_color * lower_color

                        IMGS = float_to_int(IMGS, dtype=dtype)
                        for i in range(shape[0]):
                            mask = cv2.inRange(src=IMGS[i], lowerb=lower_color, upperb=upper_color)
                            IMGS[i, mask > 0] = [255, 255, 255]
                    except TypeError:
                        error = init.bold + fg.rbg(0, 255, 0) + f"data type error in {fg.rbg(255,0,0)}<<upper_color>> or <<lower_color>>" + init.reset
                        print(error)
                else:
                    error = init.bold + fg.rbg(0, 255, 0) + f"{fg.cyan_L}len(upper_color) != {shape[-1]}" + init.reset
                    print(error)
            else:
                error = init.bold + fg.rbg(0, 255, 0) + f"{fg.cyan_L}len(upper_color) != len(lower_color)" + init.reset
                print(error)
        else:
            error = init.bold + fg.rbg(0, 255, 0) + f"upper_color cannot be empty" + init.reset
            print(error)
    else: 
        t = type(np.array([0]))
        error = init.bold + fg.rbg(0, 255, 0) + f"imgs {fg.white_L} is not {fg.rbg(255,0,0)}{t}" + init.reset
        print(error)

    return IMGS

def filter_selection(
        img             : [list, np.ndarray], 
        figsize         : tuple  = (15, 4), 
        color_indexes   : list   = [30, 60, 25], 
        mul             : float  = 1.0,
        names           : list   = [], 
        select_index    : list   = [0],
        xlabel          : str    = "Bins",
        ylabel          : str    = "Fréquences",
        bins            : int    = 255,
        rwidth          : float  = 0.2
        ):

    """
    Copyright : Iréné A. Essomba (c) 2023


    * img is the image with (n, m, m, 3) dimension, where n is the samples
    * figsize is a tuple used to create figures 
    * color_indexes is a list of size 3 used to set color in each plot
    * mul is numeric value
    * names is a list that contains the names of speces len(names) = n 
    
    *----------------------------------------------------------
    
    >>> img     = np.random.randn(3, 160, 160, 3)
    >>> names   = ["A", "B", "C"]
    >>> filter_selection(img = img, fisize = (8, 8), color_indexes = [20, 10,  6], names=names)
    
    """
    import matplotlib.pyplot as plt 
    import matplotlib.colors as mcolors

    # uploading all python colors
    colors = list(mcolors.CSS4_COLORS.keys())
    # get the channel of the image
    #channel = img.shape[-1]
  
    # plotting image in function of the channel
    lenght = len(select_index)
    fig, axes = plt.subplots(lenght, 3, figsize=figsize, sharey=True)

    for i in range(lenght):
        if i in select_index:
            channel = img[i].shape[-1]
            for j in range(channel):
                axes[i, j].hist(img[i][:, :, j].ravel() * mul, bins=bins, color=colors[color_indexes[j]], histtype="bar", 
                                rwidth=rwidth ,density=False)
                # title of image
                if i == 0: axes[i, j].set_title(f"axis {j}", fontsize="small")
                # set xlabel
                if i == lenght-1 :axes[i, j].set_xlabel(xlabel, weight="bold")
                # set ylabel
                if j == 0 :  axes[i, j].set_ylabel(ylabel, weight="bold")

                axes[i, j].legend(labels = [names[i]], fontsize='x-small')
        else: pass
    plt.show()


