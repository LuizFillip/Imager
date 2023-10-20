import imager as im
import os




def process_all_images(files): 
    
    files  = [f for f in files if f.endswith("tif")]
    
    for fname in files:
        
        save_in = fname.replace("tif", "png")
        
        name = os.path.split(save_in)[-1]
        print("[process_images]", name)
    
        im.save_img(im.processing_img(fname), save_in)
        
          

#process_all_images(files)

infile = 'D:\\img\\CA_2013_0104\\'

files = os.listdir(infile)

process_all_images(files)