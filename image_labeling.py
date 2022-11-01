import cv2
import os
import matplotlib.pyplot as plt
from image_settings import processing, get_files
from image_utils import imager_fname
import numpy as np
import datetime
import os
from PIL import Image, ImageDraw, ImageFont

def draw_labels(ax, 
                filename, 
                fontsize = 20, 
                color = "black"):
    
    d = imager_fname(filename)
    
    ax.text(12, 500, d.time, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(360, 500, d.date, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(12, 30, d.site, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(470, 30, d.emission, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(230, 45, "N", 
            transform = ax.transData, 
            color = color, fontsize = fontsize + 10)
    ax.text(480, 270, "E", 
            transform = ax.transData, 
            color = color, fontsize = fontsize + 10)
    
   
def remove_ticks(ax):
    
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
        
        
infile = "C:\\observation\\172\\imager\\"


files = get_files(infile)

filename = files[0]

img = processing(infile + filename).all_processing

plt.imshow(img)