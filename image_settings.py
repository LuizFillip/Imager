import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
from utils import filename_to_datetime



def setting_brightness(img, alpha = 6.0, beta = 4.0):
    
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    
    return cv2.flip(image, 1)


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
    
    
    ax.text(400, 500, f"{date_time.date()} UT", 
            transform = ax.transData, 
            color = "white", fontsize = 20)
    
    ax.set(xticks = [], yticks = [])
    
    if save:
        print("saving...", filename)
        fig.savefig(path_to_save + filename, 
                    dpi = 100, 
                    bbox_inches="tight")
    else:
        plt.show()
        
        
infile = "database/2014/001/"
_, _, files = next(os.walk(infile))


path_to_save = "database/2014/001_test/"

filename = files[45]
#for filename in files:
    
image_with_labels(infile, filename, 
                      path_to_save= path_to_save, 
                      save = False)


