import cv2
import os
import matplotlib.pyplot as plt
from image_settings import load_and_processing
from image_utils import imager_fname
import numpy as np
import datetime
import os
from PIL import Image, ImageDraw, ImageFont

def draw_labels(ax, 
                filename, 
                fontsize = 20, 
                color = "black", 
                site = "CA", 
                emisson = "O6"):
    
    d = imager_fname(filename)
    
    ax.text(30, 510, d.time, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(390, 510, d.date, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(30, 20, site, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(470, 20, emisson, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(260, 45, "N", 
            transform = ax.transData, 
            color = "white", fontsize = fontsize + 10)
    
    ax.text(260, 500, "S", 
            transform = ax.transData, 
            color = "white", fontsize = fontsize + 10)
    
    ax.text(45, 270, "O", 
            transform = ax.transData, 
            color = "white", fontsize = fontsize + 10)
    
    ax.text(480, 270, "E", 
            transform = ax.transData, 
            color = "white", fontsize = fontsize + 10)
    
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.left.set_visible(False)
    ax.spines.bottom.set_visible(False)

    ax.set(xticks = [], yticks = [])
    
    
    
def image_visualization(infile, filename, 
                        path_to_save = "",
                        save = False):
    
    img = load_and_processing(infile, filename)
    

   
    if save:
        plt.ioff()
    
    fig, ax = plt.subplots(figsize = (10, 10))
    
    ax.imshow(img)
    
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.left.set_visible(False)
    ax.spines.bottom.set_visible(False)

    ax.set(xticks = [], yticks = [])
    
    
    if save:
        print("saving...", filename)
        fig.savefig(path_to_save + filename, 
                    dpi = 100,pad_inches = 0, 
                    bbox_inches="tight", 
                    transparent=True)
    else:
        plt.show()
        
        
