import cv2
import matplotli.pyplot as plt

from image_settings import setting_brightness
from utils import imager_fname



def image_visualization(infile, filename, path_to_save = "",
                      save = False):
    
    
    image_read = cv2.imread(infile + filename)
    imagem = setting_brightness(image_read, 
                                alpha = 6, beta = 2)
   
    
    if save:
        plt.ioff()
    
    fig, ax = plt.subplots(figsize = (10, 10))
    
    ax.imshow(imagem)
    
    if save:
        print("saving...", filename)
        fig.savefig(path_to_save + filename, 
                    dpi = 100, 
                    bbox_inches="tight", 
                    transparent=True)
    else:
        plt.show()
        
        
def draw_labels(ax, filename):
    
    date_time = imager_fname(filename)
    
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