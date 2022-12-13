import cv2
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from calibrate import find_calibration
from image_utils import imager_fname
from skimage import io
from base import getlevel2, bytscl2


def int45(A):
    B = abs(A)
    C = B + 0.5
    return (A / abs(A)).astype(int)*C.astype(int)


class image_processing(object):
    
    def __init__(self, fname):

        read = cv2.imread(fname)
        self.img = cv2.cvtColor(read, cv2.IMREAD_GRAYSCALE)
   
        
        
    @staticmethod  
    def constrast_adjust(img, alpha = 4, beta = 1.1):
        return cv2.convertScaleAbs(img, 
                                   alpha = alpha, 
                                   beta = beta)
    
    @staticmethod
    def get_level(filt_img, sref_min = 0.0099, sref_max = 0.9): 
        variavel = getlevel2(filt_img, sref_min, sref_max)
        return bytscl2(filt_img, variavel[1], variavel[0])
    
    
    def all_processing(self, alpha = 6, beta = 1.3, 
                       sref_min = 0.009, sref_max = 0.9):

        image = self.constrast_adjust(self.img,  
                                      alpha = alpha, 
                                      beta = beta)    
        return image


def rotated(image, fname):
    
    
    time = imager_fname(fname).datetime
    
    dat = find_calibration(time)
    angle = float(dat["Rotation"])

    if dat["Horizontal Flip"] == "ON":
        image = cv2.flip(image, 1)
    elif dat["Vertical   Flip"] == "ON":
        image = cv2.flip(image, 1)
        
    (h, w) = image.shape[:2]
    
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return Image.fromarray((rotated * 1).astype(np.uint8)).convert('RGB')


     
def main():
    fname = "O6_CA_20160105_014705.tif" 
    
    img = image_processing(fname).all_processing()
    plt.imshow(img)
    
    