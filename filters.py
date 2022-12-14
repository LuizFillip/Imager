import numpy as np
from skimage import io
from constants import constants as c
from mapping import lens_function, get_attributes
import matplotlib.pyplot as plt


fname = "database/examples/OH_CA_20181112_002024.tif" 


img = io.imread(fname, as_gray = True)


xsize, ysize = img.shape

Re = c.equator_radius
a = 0.2
Ftheta = 0

attrs = get_attributes(fname)
xm = attrs.xm
ym = attrs.ym

z = np.arange(91) * 0.5* (np.pi/180)
fitting = lens_function(z, attrs)

plt.plot(z, fitting)



def vanRhijn_atmExtinsion():
    
    vr = np.zeros((xsize, ysize))
    ae = np.zeros((xsize, ysize))
    ang = np.zeros((xsize, ysize))
    ang2 = np.zeros((xsize, ysize))

    
    height = c.emission_band()
    
    for i in range(0, xsize - 1):
        for j in range(0, ysize - 1):
            
            dx = np.sqrt((i - xm)**2 + (j - ym)**2)
           
           
            angulo = (attrs.a0 + 
                      attrs.a1*dx + 
                      attrs.a2*dx**2 + 
                      attrs.a3*dx**3 + 
                      attrs.a4*dx**4)
           
            ang[i, j] = np.radians(angulo)
            
            
            vr[i, j] = (1 - (Re / (Re + height)**2)*(np.sin(ang[i, j]))**2)**(-0.5)
           
            Ftheta = (np.cos(ang[i, j]) + (0.15 * ((93.885 - angulo)**(-1.253))))**(-1)
           
            ae[i, j] = 10**(-0.4 * a * Ftheta)
        
    id_ = np.where(ang > 90, )


