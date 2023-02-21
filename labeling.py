import os
import matplotlib.pyplot as plt
from AllSky.image_utils import imager_fname

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
    
   
def save_img(fig, 
             save_in):
    
    plt.ioff()
    
    fig.savefig(save_in, 
                pad_inches = 0, 
                bbox_inches = "tight", 
                transparent = True)
    plt.clf()   
    plt.close()
    return 

def visualization(image, 
                  infile,
                  width = 12, 
                  height = 12):
    
    """Read, processing and save it"""
    

    fig = plt.figure(figsize = (width, height), dpi = 100)
    ax = fig.add_subplot()
    
    ax.imshow(image, cmap = "gray")
    
    ax.set_axis_off()
    
    #ax.margins(0)
    
    draw_labels(ax, 
                infile, 
                fontsize = 20, 
                color = "white")

    plt.show()
    
    return fig
   
def main():     
    infile =  "database/examples/OH_CA_20181112_002024.tif" 
            
    image, fig = visualization(infile)
        