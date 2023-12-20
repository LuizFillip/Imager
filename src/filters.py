import numpy as np
from skimage import io
import imager as im
from scipy.ndimage import median_filter





def remove_stars(
        image, 
        starsize = 5, 
        threshold = 50
        ):
    
    a_filtered = median_filter(
        image, size = starsize)

    a_final = np.where(
        (image - a_filtered) > threshold, 
        a_filtered, image)

    return a_final


def getlevel(array, sref):
    a = np.uint16(array)
    
    hist, _ = np.histogram(
        a, bins = np.max(a) + 1)

    slevels = np.zeros(len(sref), dtype=float)

    sa = np.uint64(0)

    for j in range(len(sref)):
        sa = sref[j] * np.sum(hist)
        #get maximum argument of cummulative sum
        idx = np.argmax(np.cumsum(hist) >= sa)
        slevels[j] = idx

    return slevels



def bytscl(array, max_slevel, min_slevel):
    top = np.uint16(2**16 - 1)  # Top value of a 16-bit array
    scaled_array = np.clip(
        ((top + 1) * (array - min_slevel - 1) / 
         (max_slevel - min_slevel)), 0, top)
    
    scaled_array[array > max_slevel] = top
    scaled_array[array < min_slevel] = 0
    
    return scaled_array



def contrast_adjust(img, limits = [0.2, 0.95]):
    """Apply get level and bytescale into an image"""
    slevels = getlevel(img, limits)
    
    return bytscl(img, slevels[1], slevels[0])


def main():

    fname = "database/examples/OH_CA_20181112_002024.tif" 
    
    img = io.imread(fname, as_gray = True)
    
    ae, vr = vanRhijn_atmExtinction(img, a = 0.2, Ftheta = 0)

import numpy as np

def calculate_angles(img, fname, height):
    Re = 6730  # Assuming the constant value of Re

    attrs = im.get_attributes(fname)
    xm, ym = attrs.xm, attrs.ym

    xsize, ysize = img.shape
    z = np.arange(181) * 0.5 * (np.pi / 180)
    fitting = np.polyfit(
        im.lens_function(z, attrs),
        z * 180 / np.pi, 4)[::-1]

    ang = np.zeros((xsize, ysize))

    for i in range(xsize):
        for j in range(ysize):
            dx = np.sqrt((i - xm) ** 2 + (j - ym) ** 2)

            ang[i, j] = (fitting[0] +
                         fitting[1] * dx +
                         fitting[2] * dx ** 2 +
                         fitting[3] * dx ** 3 +
                         fitting[4] * dx ** 4)
    return ang

def vanRhijn(img, fname, Ftheta=0, height=250):
    Re = 6730  # Assuming the constant value of Re

    ang = calculate_angles(img, fname, height)

    xsize, ysize = img.shape
    vr = np.zeros((xsize, ysize))
    
    for i in range(xsize):
        for j in range(ysize):
            sin_ang = np.sin(np.radians(ang[i, j]))
            vr[i, j] = 1 / np.sqrt(1 - (Re / (Re + height) ** 2) * sin_ang ** 2)

           
    return vr

def atmExtinction(img, fname, height = 250, a=0.2,):
    
    xsize, ysize = img.shape
    ae = np.zeros((xsize, ysize))
    
    ang = calculate_angles(img, fname, height)

    for i in range(xsize):
        for j in range(ysize):
            cos_ang = np.cos(np.radians(ang[i, j]))
            Ftheta = 1 / (cos_ang + 0.15 * 
                          (93.885 - ang[i, j]) ** -1.253)
            
            ae[i, j] = 10 ** (-0.4 * a * Ftheta)
        
            if ang[i, j] > 90:
                ae[i, j] *= 0  
    
    return ae