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
from config import init, fg, bg                                                          #
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
    
def image_processing( image : np.ndarray, name : str = "RGB", reshape : tuple = (160, 160)):
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
    elif name == "RGR2-LAB"     : filter = cv2.cvtColor(imgs, cv2.COLOR_BGR2LAB)
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

