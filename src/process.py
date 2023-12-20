import imager as im
import base as b 
import os
import matplotlib.pyplot as plt


def save_img(fig, 
             save_in):
    
    fig.savefig(
        save_in, 
        dpi = 400, 
        pad_inches = 0, 
        bbox_inches = "tight", 
        transparent = False
        )
    
    plt.clf()   
    plt.close()
    return 



def process_visualize(
        path_in, 
        size = 10,
        stars = False
        ):
    
    image = im.processing_img(
        path_in, 
        hori_flip = True,
        vert_flip = False
        )
    if stars:
        img_pro = im.remove_stars(image)
    else:
        img_pro = image
        
    return im.visualization(
                path_in, 
                img_pro, 
                width = size, 
                height = size
            )



def process_img_to_img(path_folder, folder_out):
    
    for fname in os.listdir(path_folder):
        
        if 'DARK' not in fname:
        
            path_in = os.path.join(
                path_folder, 
                fname
                )
            
            save_in = os.path.join(
               folder_out, 
               fname.replace('tif', 'png')
               )
            
            print('[processing image]', fname)
            
            fig = process_visualize(path_in)
            
            save_img(fig, save_in)
      
def process_folder_to_folder(
        PATH_IN, 
        PATH_OUT
        ):
                
    plt.ioff()
    
    for folder in os.listdir(PATH_IN):
        
        folder_out = os.path.join(
             PATH_OUT, 
             folder
             )
        
        cond = os.path.exists(
            os.path.join(PATH_OUT, folder)
            )
        
        if cond == False:
            b.make_dir(folder_out)
            
            path_folder = os.path.join(
                PATH_IN, folder
                )
            
            process_img_to_img(
                path_folder, folder_out
                )
            
    plt.clf()   
    plt.close()
    
# process_folder_to_folder(
#         PATH_IN, 
#         PATH_OUT
#         )

path_in = 'D:\\img\\CA_2017_0403\\'
path_out = 'D:\\img\\CA_2017_0403P\\'
process_img_to_img(
    path_in, path_out
    )