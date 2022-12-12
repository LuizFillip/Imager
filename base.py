import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
from PIL import Image, ImageDraw, ImageFont
from calibrate import find_calibration
from image_utils import imager_fname

def getlevel(array, sref):
    # array : array input
    # sref : reference ratio levels
    # slevels : output levels

    a = np.uint16(array)
    maximo = np.amax(a)

    hist, _ = np.histogram(a, range=(0, maximo), bins= maximo+1)

    ksize = len(hist)
    ta = np.sum(hist)

    ssize = len(sref)
    slevels = np.zeros(ssize, dtype=float)

    sa, i = np.uint64(0), np.uint64(0)
      
    while i < ksize-1:
        i += 1
        sa = sa + hist[int(i)]
        for j in range(ssize):
            if sa < sref[j]*ta:
                slevels[j]=i

    return slevels

def bytscl(array, max_slevel, min_slevel):
    top = np.uint16(2**16-1) #Top value of an array of 16bits

    dim_x, dim_y = array.shape
    for j in range(dim_x):
        for i in range(dim_y):
            if min_slevel<=array[i,j]<=max_slevel:
                array[i,j] = (top+1)*(array[i,j]-min_slevel-1)/(max_slevel-min_slevel)
            elif array[i,j]>max_slevel:
                array[i,j]=top
            elif array[i,j]<min_slevel:
                array[i,j]=0
    
    return array





