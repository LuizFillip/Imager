import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
from PIL import Image, ImageDraw, ImageFont


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

def setting_brightness(img, alpha = 6.0, beta = 2.0):
    
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    
    return cv2.flip(image, 1)


def image_processing(infile, filename):
    
    read = cv2.imread(infile + filename, cv2.COLOR_BGR2RGB)
    imagem = setting_brightness(read, alpha = 6, beta = 2.0)
    
    #imagem = cv2.imread(infile + filename, cv2.COLOR_BGR2RGB)
    sref_min = 0.25 #preto
    sref_max = 0.98 #branco
    variavel = get_level(imagem, sref_min, sref_max)

    return bytscl(imagem, variavel[1], variavel[0])

        
        
def crop_image_like_circle(img):
    
    img = Image.fromarray((img * 1).astype(np.uint8)).convert('RGB')


    npImage = np.array(img)
    h, w = img.size

    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([30, 20, h, w], 0, 360, fill = 255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    npImage=np.dstack((npImage, npAlpha))
    
    return Image.fromarray(npImage)


def image_with_labels(infile, filename, path_to_save = "",
                      save = False):
        
    imagem = setting_brightness(cv2.imread(infile + filename), 
                                alpha = 6, beta = 2)
   
    
    if save:
        plt.ioff()
    
    fig, ax = plt.subplots(figsize = (10, 10))
    
    ax.imshow(imagem)
    
    date_time = filename_to_datetime(filename)
    
    ax.text(5, 500, f"{date_time.time()} UT", 
            transform = ax.transData, 
            color = "white", fontsize = 20)
    
    
    ax.text(400, 500, f"{date_time.date()}", 
            transform = ax.transData, 
            color = "white", fontsize = 20)
    
    
    ax.text(10, 50, f"CA", 
            transform = ax.transData, 
            color = "white", fontsize = 40)
    
    ax.set(xticks = [], yticks = [])
    
    if save:
        print("saving...", filename)
        fig.savefig(path_to_save + filename, 
                    dpi = 100, 
                    bbox_inches="tight", 
                    transparent=True)
    else:
        plt.show()
        
        
infile = "database/2014/001/"
_, _, files = next(os.walk(infile))


path_to_save = "database/2014/001_test/"

#filename = files[45]
for filename in files:
    
    image_with_labels(infile, 
                      filename, 
                      path_to_save = path_to_save, 
                      save = True)


