import os
import matplotlib.pyplot as plt
from base import getlevel, bytscl
from image_utils import imager_fname
from skimage import io

def draw_labels(ax, 
                infile, 
                fontsize = 20, 
                color = "black"):
    
    filename = os.path.split(infile)[-1]
    
    d = imager_fname(filename)
    
    ax.text(0, 510, d.str_time, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(390, 510, d.str_date, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(0, 15, d.site, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(480, 15, d.emission, 
            transform = ax.transData, 
            color = color, fontsize = fontsize)
    
    ax.text(256, 15, "N", 
            transform = ax.transData, 
            color = color, fontsize = fontsize + 10)
    ax.text(490, 256, "E", 
            transform = ax.transData, 
            color = color, fontsize = fontsize + 10)
    
   
def save(fig, 
         filename, 
         path_to_save = ""):
    
    print("saving...", filename)
    
    plt.ioff()
    
    fig.savefig(path_to_save + filename, 
                pad_inches = 0, 
                bbox_inches = "tight", 
                transparent = True)
    plt.clf()   
    plt.close()
    return 

def visualization(infile, 
                  width = 9, 
                  height = 9):
    
    """Read, processing and save it"""
    
    img = io.imread(infile)
    
    slevels = getlevel(img, [0.2, 0.95])

    new_img = bytscl(img, 
                      slevels[1], 
                      slevels[0])
            
    fig, ax = plt.subplots(figsize = (width, height))
    
    ax.imshow(new_img, cmap = "gray")
    
    ax.set_axis_off()
    
    draw_labels(ax, 
                infile, 
                fontsize = 20, 
                color = "white")

    plt.show()
    
    return fig
        
infile =  "database/examples/O6_CA_20181112_000244.tif" 
        
visualization(infile)
        
