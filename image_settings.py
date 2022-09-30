import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
from PIL import Image, ImageDraw, ImageFont
from calibrate import find_calibration
from image_utils import imager_fname

def bytscl(array, max = None, min = None, nan = 0, top=255):
    # see http://star.pst.qub.ac.uk/idl/BYTSCL.html
    # note that IDL uses slightly different formulae for bytscaling floats and ints.
    # here we apply only the FLOAT formula...

    if max is None: max = np.nanmax(array)
    if min is None: min = np.nanmin(array)

    # return (top+0.9999)*(array-min)/(max-min)
    return np.maximum(np.minimum(
        ((top + 0.9999) * (array - min) / (max - min)).astype(np.int16)
        , top), 0)


def get_level(im2, sref_min, sref_max):
    '''
    :param im2: imagem tipo float
    :param sref_min: nivel de referencia normalizado
    :param sref_max: nivel de referencia normalizado
    :return: limites inferior e superior da imagem para exibição na tela, 
    baseado nos niveis de referencia.
    '''
    #
    x_min, x_max = np.min(im2), np.max(im2)

    # bin_size precisa ser 1 para analisar ponto à ponto
    bin_size = 1
    x_min = 0.0

    nbins = np.floor(((x_max - x_min) / bin_size))

    try:
        hist, bins = np.histogram(im2, int(nbins), range=[x_min, x_max])

        sum_histogram = np.sum(hist)

        sref = np.zeros(2)
        sref[0] = sref_min
        sref[1] = sref_max

        res_sa = np.zeros(len(hist))

        sa = 0.
        for i in range(len(hist)):
            sa += hist[i]
            res_sa[i] = sa

        res_sa2 = res_sa.tolist()
        res = res_sa[np.where((res_sa > sum_histogram * sref[0]) & (res_sa < sum_histogram * sref[1]))]
        nr = len(res)

        sl0 = res_sa2.index(res[0])
        sl1 = res_sa2.index(res[nr - 1])
        slevel = [sl0, sl1]
    except Exception as e:
        print("Exception get_level ->" + str(e))
        print("slevel = [10, 20]")
        slevel = [10, 20]

    return slevel





def rotate(image, time, 
           center = None, 
           scale = 1.0, 
           flip = "ON"):
    
    dat = find_calibration(time)
    angle = float(dat["Rotation"])
    flip = dat["Horizontal Flip"]
    
    if flip == "ON":
        image = cv2.flip(image, 1)
    
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    
    return Image.fromarray((rotated * 1).astype(np.uint8)).convert('RGB')

def load_and_processing(filename, 
                        alpha = 4.0, 
                        beta = 1.1, 
                        sref_min = 0.0099, 
                        sref_max = 0.9):
    
    time = imager_fname(filename).datetime
    
    read = cv2.imread(filename)
    img = cv2.cvtColor(read, cv2.IMREAD_GRAYSCALE)
    
    filt_img = cv2.convertScaleAbs(img, alpha = alpha, beta = beta)
    
    variavel = get_level(filt_img, sref_min, sref_max)
    
    img_rotated = rotate(bytscl(filt_img, variavel[1], variavel[0]), time)

    return img_rotated


        
def crop_image_like_circle(img):
    
    img = Image.fromarray((img * 1).astype(np.uint8)).convert('RGB')


    npImage = np.array(img)
    h, w = img.size

    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([30, 20, h, w], 0, 360, fill = 255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    npImage=np.dstack((npImage, npAlpha))
    
    return Image.fromarray(npImage)

def crop_like_an_rectangle(img, x = 30, y = 20):
    img = np.array(img)                                              
    h = img.shape[0]
    w = img.shape[1]
    return img[y:y+h, x:x+w]




        
  

