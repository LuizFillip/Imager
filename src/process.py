import imager as im
import base as b 
import os 

def process_visualize(path_in, size = 10):
    image = im.processing_img(
        path_in, 
        hori_flip = False,
        vert_flip = True
        )
    
    
    return im.visualization(
                im.remove_stars(image), 
                path_in, 
                width = size, 
                height = size
                )


infile = 'D:\\img\\'

for folder in os.listdir(infile)[:-1]:
    
    folder_out =  path_out = os.path.join(
         'D:\\img\\PRO\\', 
         folder
         )
    
    b.make_dir(folder_out)
    
    
    path_folder = os.path.join(infile, folder)
        
    for fname in os.listdir(path_folder):
        
        if 'DARK' in fname:
            pass
        else:
        
            path_in = os.path.join(path_folder, fname)
            
    
            save_in = os.path.join(
               folder_out, 
               fname.replace('tif', 'png')
               )
            
            
            print('processing', fname)
            fig = process_visualize(path_in, size = 10)
            
            save_img(fig, save_in)