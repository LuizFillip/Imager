import matplotlib.pyplot as plt
import numpy as np
import base as b
from skimage import exposure, io
import imager as im 

'''
Histogram Equalization
'''


b.config_labels(fontsize = 15)

# Load an example image

fname = 'imager/img/O6_CA_20160211_232747.tif'
img = io.imread(fname, as_gray = True)


# Contrast stretching
p2, p98 = np.percentile(img, (2, 98))

img_rescale = exposure.rescale_intensity(img, in_range=(p2, p98))

# Equalization
img_eq = exposure.equalize_hist(img)

# Adaptive Equalization
img_adapteq = exposure.equalize_adapthist(img, clip_limit = 0.1)

names= ['Low contrast image',
        'Contrast stretching', 
        'Histogram equalization', 
        'Adaptive equalization']

images = [img, img_rescale, img_eq, img_adapteq]

def display_results(images, names):
        
    fig, ax = plt.subplots(
        ncols = len(images), 
        dpi = 300, 
        figsize = (14, 8)
        )
    
    plt.subplots_adjust(wspace = 0.05)
    
    for i, ax_img in enumerate(ax.flat):
        
        im.display_image(images[i], names[i])
        
        
    return fig

fig = display_results(images, names)