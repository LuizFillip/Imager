import imager as im
import os
from skimage import io
import numpy as np



def process_all_images(files): 
    
    files  = [f for f in files if f.endswith("tif")]
    
    for fname in files:
        
        save_in = fname.replace("tif", "png")
        
        name = os.path.split(save_in)[-1]
        print("[process_images]", name)
    
        im.save_img(processing_img(fname), save_in)
        
          

#process_all_images(files)
fname = 'imager/img/O6_CA_20160211_232747.tif'
fn = processing_img(fname)
