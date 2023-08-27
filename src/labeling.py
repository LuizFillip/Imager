import os
import matplotlib.pyplot as plt
import datetime as dt


class imager_fname(object):
    
    """Get datetime from filename (EMBRACE format)"""
    
    def __init__(self, filename):
        
        filename = os.path.split(filename)[-1]
  
        infos = filename[:-4].split("_")
        date = infos[2]
        time = infos[-1]
        self.emission = infos[0]
        self.site = infos[1]
        self.datetime = dt.datetime.strptime(
            date + " " + time, 
            '%Y%m%d %H%M%S')
  
    @property
    def str_time(self):
        return self.datetime.strftime("%H:%M:%S UT")
    
    @property
    def str_date(self):
        return self.datetime.strftime("%d/%m/%Y")

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
                dpi = 100, 
                pad_inches = 0, 
                bbox_inches = "tight", 
                transparent = False)
    plt.clf()   
    plt.close()
    return 

def visualization(
        image, 
        infile,
        width = 12, 
        height = 12
        ):
    
    """Read, processing and save it"""
    

    fig = plt.figure(
        figsize = (width, height), 
        dpi = 300
        )
    ax = fig.add_subplot()
    
    ax.imshow(image, cmap = "gray")
    
    ax.set_axis_off()
        
    draw_labels(
        ax, 
        infile, 
        fontsize = 20, 
        color = "white"
        )

    plt.show()
    
    return fig
   
def main():     
    infile =  "database/examples/OH_CA_20181112_002024.tif" 
            
    image, fig = visualization(infile)
        