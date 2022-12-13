from processing import image_processing
import matplotlib.pyplot as plt
import numpy as np
from calibrate import find_calibration
from image_utils import imager_fname
from constants import constants as c




class get_attributes:

    def __init__(self, fname):
        time = imager_fname(fname).datetime
        dat = find_calibration(time)
        
        
        self.lat_obs = np.radians(float(dat["Latitude"]))
        self.alt_obs = float(dat["Altitude"]) / 1000
        self.xm = float(dat["Zenith x"])
        self.ym = float(dat["Zenith y"])
        
        self.a0 = float(dat["A0"])
        self.a1 = float(dat["A1"])
        self.a2 = float(dat["A2"])
        self.a3 = float(dat["A3"])
        self.a4 = float(dat["A4"])

        self.rotation = np.radians(float(dat["Rotation"]))
        
    @property
    def erad(self):
        
        eq = c.equator_radius
        ep = c.polo_radius
        
        num = pow(eq * ep, 2)
        den = (pow(eq * np.sin(self.lat_obs), 2) + 
               pow(ep * np.cos(self.lat_obs), 2.0))
        return np.sqrt(num / den)

def lens_function(dat):
    
    """
    Lens function with fitting coefficients
    """

    fitt_coeficients = [float(dat[item]) for item in 
                        ['A0', 'A1', 'A2', 'A3', 'A4']]
    fitt_coeficients = np.array(fitt_coeficients, np.float32)

    return np.poly1d(fitt_coeficients)

def load(fname):
    
    img = image_processing(fname).all_processing()
    
    return np.array(img)[:, :, 0]

def projection_factor(size_x = 512, 
                      proj_area = 512):
    return proj_area / size_x





def make_mapping(original):
    
    
    attrs = get_attributes(fname)
    
    alpha = projection_factor()

    alt_ag = c.emission_band()
            
    size_x, size_y = original.shape[:]
    half_x, half_y = (size_x - 1) / 2.0, (size_y - 1) / 2.0
    
    
    xx = np.zeros((size_x, size_y))
    yy = np.zeros((size_x, size_y))
    az = np.zeros((size_x, size_y))
    rr = np.zeros((size_x, size_y))
    a = np.zeros((size_x, size_y))
    ze = np.zeros((size_x, size_y))
    rrr = np.zeros((size_x, size_y))
    
    imgmap = np.zeros((2, size_x, size_y), 
                      dtype=np.int16)
    
    
    for i in range(size_x):
        for j in range(size_y):
            
            if (i == half_x) and (j == half_y):
                xx[i, j] = attrs.xm
                xx[i, j] = attrs.ym
                
            az[i, j] = np.arctan2(half_x - i, half_y - j)
            
            if az[i,j] < 0:
                az[i,j] = 2*np.pi + az[i,j]
                
                
            rr[i, j]= np.sqrt(pow(half_x - i, 2) + 
                              pow(half_y - j, 2))
            
            a[i,j] =  rr[i,j] * alpha / ( attrs.erad + alt_ag)
            ze[i,j] = np.arctan2((attrs.erad + alt_ag) * np.sin(a[i, j]), 
                                 (attrs.erad + alt_ag) * np.cos(a[i, j]) - 
                                 (attrs.erad + attrs.alt_obs))
            
            rrr[i,j] = (attrs.a0 + 
                        attrs.a1*ze[i,j] + 
                        attrs.a2*ze[i,j]**2 + 
                        attrs.a3*ze[i,j]**3 + 
                        attrs.a4*ze[i,j]**4)
            
            xx[i,j] = attrs.xm - rrr[i,j] * np.sin(az[i,j] - attrs.rotation)
            yy[i,j] = attrs.ym + rrr[i,j] * np.cos(az[i,j] - attrs.rotation)
            
            if ((xx[i,j] >= 0) and 
                (yy[i,j] >= 0) and 
                (xx[i,j] <= size_x - 1) and 
                (yy[i,j] <= size_x - 1)):
            
              imgmap[0,i,j] = xx[i,j]
              imgmap[1,i,j] = yy[i,j]

    return imgmap



def linearization(original, 
                  mapping, 
                  horizontal_flip = True):
    
    _, size_x, size_y = mapping.shape
    
    map_x = mapping[0, 0: size_x - 1, 0: size_y - 1]
    map_y = mapping[1, 0: size_x - 1, 0: size_y - 1]
    
    new_img = original[map_x, map_y] 
    
    if horizontal_flip:
        
        new_img = np.flipud(new_img)
    
    return new_img


fname = "database/examples/O6_CA_20181112_000244.tif" 

original = load(fname)

imgmap = make_napping(original)
img = linearization(original, 
                    imgmap)
plt.imshow(img)