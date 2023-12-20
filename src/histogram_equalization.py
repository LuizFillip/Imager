
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from skimage import data, img_as_float, io
from skimage import exposure


matplotlib.rcParams['font.size'] = 8

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

# Display results
fig, ax = plt.subplots(
    ncols = 4, 
    dpi = 300, 
    figsize = (12, 6)
    )

plt.subplots_adjust(wspace = 0.05)

names= ['Low contrast image', 'Contrast stretching', 
        'Histogram equalization', 'Adaptive equalization']

images = [img, img_rescale, img_eq, img_adapteq]
for i, ax_img in enumerate(ax.flat):
    
    ax_img.imshow(images[i], cmap=plt.cm.gray)
    ax_img.set_axis_off()
    ax_img.set(title = names[i])
