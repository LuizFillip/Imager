import imager as im
import os
from skimage import io


def processing_img(fname):
    
    img = io.imread(fname, as_gray = True)
    
    img2 = im.rotated(img, fname)
    
    slevels = im.getlevel(img2, [0.3, 0.94])
    
    new_img = im.bytscl(
        img2, 
        slevels[1], 
        slevels[0])
      
    return im.visualization(new_img, fname, 
                            width = 10, 
                            height = 10)

def process_all_images(files): 
    
    files  = [f for f in files if f.endswith("tif")]
    
    for fname in files:
        
        save_in = fname.replace("tif", "png")
        
        name = os.path.split(save_in)[-1]
        print("processing...", name)
    
        im.save_img(processing_img(fname), save_in)
        
          

#process_all_images(files)
fname = 'imager/img/O6_CA_20160211_232747.tif'
processing_img(fname)
