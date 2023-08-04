# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 12:57:38 2023

@author: Luiz
"""


import matplotlib.pyplot as plt
from skimage import io
from imager.src.base import getlevel, bytscl

def get_level(filt_img, sref_min = 0.0099, sref_max = 0.9): 
    variavel = getlevel(filt_img, sref_min)
    return bytscl(filt_img, variavel[1], variavel[0])


fname = "database/AllSky/examples/OH_CA_20181112_002024.tif" 

img = io.imread(fname, as_gray = True)

plt.imshow(get_level(img), cmap = 'gray')