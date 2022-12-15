import numpy as np
from skimage import io
from constants import constants as c
from mapping import lens_function, get_attributes, linearization
import matplotlib.pyplot as plt
from base import getlevel, bytscl



fname = "database/examples/OH_CA_20181112_002024.tif" 

img = io.imread(fname, as_gray = True)


def vanRhijn_atmExtinction(img, a = 0.2, Ftheta = 0):
    
    xsize, ysize = img.shape

    Re = c.equator_radius

    attrs = get_attributes(fname)
    xm = attrs.xm
    ym = attrs.ym

    z = np.arange(181) * 0.5* (np.pi/180)

    fitting = np.polyfit(lens_function(z, attrs), z*180/np.pi,  4)
    fitting = fitting[::-1]
    
    vr = np.zeros((xsize, ysize))
    ae = np.zeros((xsize, ysize))
    ang = np.zeros((xsize, ysize))
    ang2 = np.zeros((xsize, ysize))
    
    height = c.emission_band()
    
    for i in range(0, xsize - 1):
        for j in range(0, ysize - 1):
            
            dx = np.sqrt((i - xm)**2 + (j - ym)**2)
          
            angulo = (fitting[0] + 
                      fitting[1]*dx + 
                      fitting[2]*dx**2 + 
                      fitting[3]*dx**3 + 
                      fitting[4]*dx**4)
           
            ang[i, j] = angulo
            
            
            vr[i, j] = (1 - (Re / (Re + height)**2)*(np.sin(np.radians(angulo)))**2)**(-0.5)
           
            Ftheta = (np.cos(np.radians(angulo)) + (0.15 * ((93.885 - angulo)**(-1.253))))**(-1)
           
            ae[i, j] = 10**(-0.4 * a * Ftheta)
            
    id_ = np.where(ang > 90)
    
    if count != 0 and id_[0] != -1:
    	ang2[id_] = 0
    	ae=ae*ang2
    return ae, vr

ae, vr = vanRhijn_atmExtinction(img, a = 0.2, Ftheta = 0)
#%%
print(img)

#%%
slevels = getlevel(img, [0.2, 0.95])
plt.imshow(bytscl(img, 
                  slevels[1], 
                  slevels[0]),
                  cmap = "gray")

