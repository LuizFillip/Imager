import matplotlib.pyplot as plt
import imager as im 
from skimage import io


file = 'database/CA_2016_0211/O6_CA_20160211_225905.tif'

dat = im.get_calibration(file)

original = io.imread(file, as_gray = True)

new_image = im.contrast_adjust(original)

img_stars = im.remove_stars(new_image)


align_axis = im.flip(im.rotate(img_stars, dat), dat)

names = ['original', 
         'contrast adjusted',
         'stars removed',
         'coords aligned']

images = [original, new_image, img_stars, align_axis] 

def display(images, names):
    
    fig, ax = plt.subplots(
        figsize = (10, 4), 
        dpi = 300,
        ncols = len(images)
        )
    
    plt.subplots_adjust(wspace = 0.1)
    
    for i, ax in enumerate(ax.flat):
        
        im.display_image(
            ax, 
            images[i], 
            title = names[i]
            )
        
    return fig
        
fig = display(images, names)

fig.savefig('imager/img/calibration')