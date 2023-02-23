from build import paths as p

from AllSky.core import rotated
from AllSky.base import getlevel, bytscl
from AllSky.labeling import visualization, save_img

from skimage import io


files = p("AllSky").get_files_in_dir("2023")



def processing_img(fname):
    
    img = io.imread(fname, as_gray = True)
    
    img2 = rotated(img, fname)
    
    slevels = getlevel(img2, [0.3, 0.94])
    
    new_img = bytscl(img2, 
                      slevels[1], 
                      slevels[0])
      
    return visualization(new_img, fname, 
                            width = 10, 
                            height = 10)
import os
def process_all_images(files): 
    
    files  = [f for f in files if f.endswith("tif")]
    
    for fname in files:
        
        save_in = fname.replace("tif", "png")
        
        name = os.path.split(save_in)[-1]
        print("processing...", name)
    
        save_img(processing_img(fname), save_in)
        
          

#process_all_images(files)


def images_to_gif():
    import glob
    import contextlib
    from PIL import Image
    
    # filepaths
    fp_in = "database/AllSky/2023/*.png"
    fp_out = "image.gif"
    
    # use exit stack to automatically close opened images
    with contextlib.ExitStack() as stack:
    
        # lazily load images
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(fp_in)))
    
        # extract  first image from iterator
        img = next(imgs)
    
        img.save(fp=fp_out, format='GIF', append_images=imgs,
                 save_all=True, duration=200, loop=0, 
                 dpi=(300, 300), quality=150)

images_to_gif()