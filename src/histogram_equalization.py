import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure, io
import imager as im 


def load_image(fname):
    
    dat = im.get_calibration(fname)
    
    img = io.imread(fname, as_gray = True)
    
    img = im.remove_stars(img)
    
    img = im.flip(im.rotate(img, dat), dat)
    
    return img


def equalization_forms(img):
    
    '''
    Histogram Equalization
    '''
    
    # Contrast stretching
    p2, p98 = np.percentile(img, (2, 99))
    
    img_rescale = exposure.rescale_intensity(
        img, in_range=(p2, p98))
    
    # Equalization
    img_eq = exposure.equalize_hist(img)
    
    # Adaptive Equalization
    img_adapteq = exposure.equalize_adapthist(
        img, clip_limit = 0.04)
    
    return [img, img_rescale, img_eq, img_adapteq]


def display_results(images, names):
        
    fig, ax = plt.subplots(
        ncols = len(images), 
        dpi = 300, 
        figsize = (14, 8)
        )
    
    plt.subplots_adjust(wspace = 0.05)
    
    for i, ax_img in enumerate(ax.flat):
        
        im.display_image(ax_img, images[i], names[i])
        
    return fig

def figure_base(fname):
    
    names= ['Low contrast image',
            'Contrast stretching', 
            'Histogram equalization', 
            'Adaptive equalization']
        
    images = equalization_forms(
        load_image(fname)
        )
    
    fig = display_results(images, names)
    
    ats = im.attributes_img(fname)
        
    fig.suptitle(
        im.str_datetime(ats['dn']), 
        y = 0.75
        )
    
    return fig

import os 
import base as b 

root = 'database/CA_2016_0211'

def process_and_save():
        
    b.make_dir(root + 'P')
    
    for fname in os.listdir(root):
        print(fname)
        plt.ioff()
        
        path = os.path.join(
            root + 'P', 
            fname
            )
        
        fig = figure_base(
            path.replace('P', '')
            )
        fig.savefig(path)
        plt.clf()   
        plt.close()