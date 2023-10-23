import numpy as np
from skimage import io
import imager as im
import cv2
from scipy.ndimage import median_filter


def int45(A):
    B = abs(A)
    C = B + 0.5
    return (A / abs(A)).astype(int)*C.astype(int)


def get_level(
        filt_img, 
        sref_min = 0.0099, sref_max = 0.9): 
    a, b = im.getlevel2(
        filt_img, 
        sref_min, 
        sref_max)
    return im.bytscl2(filt_img, a, b)
    
    
def brigthness(img, alpha = 9., beta = .09):

    return cv2.convertScaleAbs(
        img, alpha = alpha, beta = beta)
    
def rotated(image, fname):
        
    dat = im.get_calibration(fname)
    angle = float(dat["Rotation"])
    

    if dat["Horizontal Flip"] == "ON":
        image = cv2.flip(image, 1)
    elif dat["Vertical   Flip"] == "ON":
        image = cv2.flip(image, 1)
        
    image = cv2.flip(image, 0)
    (h, w) = image.shape[:2]
    
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
  
    return cv2.warpAffine(image, M, (w, h)) 

def processing_img(
        fname, 
        size = 10,
        hori_flip = True, 
        vert_flip = True 
        ):
        
    img2 = rotated(
        io.imread(fname, as_gray = True), fname
        )
    
    a, b = tuple(im.getlevel(img2, [0.2, 0.94]))
  
    new_img = im.bytscl(img2, b, a)
    
    if hori_flip: new_img = np.fliplr(new_img)
        
    if vert_flip: new_img = np.flipud(new_img)
        
      
    return new_img


def linearization(
        fname, 
        mapping, 
        horizontal_flip = True
        ):
    
    
    original = io.imread(
        fname, as_gray = True)
    
    _, size_x, size_y = mapping.shape
    
    # verificar esses indices com cristiano
    map_x = mapping[0, 0: size_x, 0: size_y]
    map_y = mapping[1, 0: size_x, 0: size_y]
    
    new_img = original[map_x, map_y] 
    
    if horizontal_flip:
        
        new_img = np.flipud(new_img)
    
    return new_img




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






