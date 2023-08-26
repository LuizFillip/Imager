import numpy as np
from skimage import io
import imager as im
import cv2


def int45(A):
    B = abs(A)
    C = B + 0.5
    return (A / abs(A)).astype(int)*C.astype(int)

        

def get_level(filt_img, sref_min = 0.0099, sref_max = 0.9): 
    variavel = im.getlevel2(filt_img, sref_min, sref_max)
    return im.bytscl2(filt_img, variavel[1], variavel[0])
    
    
def brigthness(img, alpha = 9., beta = .09):

    return cv2.convertScaleAbs(img, alpha = alpha, beta = beta)
    
def rotated(image, fname):
    
    
    time = im.imager_fname(fname).datetime
    
    dat = im.get_calibration(time)
    angle = float(dat["Rotation"])

    #if dat["Horizontal Flip"] == "ON":
     #   image = cv2.flip(image, 1)
    #elif dat["Vertical   Flip"] == "ON":
        #image = cv2.flip(image, 1)
        
    image = cv2.flip(image, 0)
    (h, w) = image.shape[:2]
    
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
  
    return cv2.warpAffine(image, M, (w, h)) 




def linearization(fname, 
                  mapping, 
                  horizontal_flip = True):
    
    
    original = io.imread(fname, as_gray = True)
    
    _, size_x, size_y = mapping.shape
    
    # verificar esses indices com cristiano
    map_x = mapping[0, 0: size_x, 0: size_y]
    map_y = mapping[1, 0: size_x, 0: size_y]
    
    new_img = original[map_x, map_y] 
    
    if horizontal_flip:
        
        new_img = np.flipud(new_img)
    
    return new_img

