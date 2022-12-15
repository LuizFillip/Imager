import matplotlib.pyplot as plt
import numpy as np
from calibrate import get_calibration
from image_utils import imager_fname
from constants import constants as c
from base import getlevel, bytscl
from skimage import io

class get_attributes:

    def __init__(self, fname):
        time = imager_fname(fname).datetime
        dat = get_calibration(time)
        
        
        self.lat_obs = np.radians(float(dat["Latitude"]))
        self.alt_obs = float(dat["Altitude"]) / 1000 # in km 
        self.xm = float(dat["Zenith x"])
        self.ym = float(dat["Zenith y"])
        
        self.a0 = float(dat["A0"])
        self.a1 = float(dat["A1"])
        self.a2 = float(dat["A2"])
        self.a3 = float(dat["A3"])
        self.a4 = float(dat["A4"])

        self.rotation = np.radians(float(dat["Rotation"]))
        
    @property
    def earth_radius(self):
        """
        Compute earth radius from a latitude
        """
        eq = c.equator_radius
        ep = c.polo_radius
        
        num = pow(eq * ep, 2)
        den = (pow(eq * np.sin(self.lat_obs), 2) + 
               pow(ep * np.cos(self.lat_obs), 2.0))
        
        return np.sqrt(num / den)

    


def lens_function(z, c):    
    """
    fourth order polynomial from fitting coefficients
    from lens function
    """
    return (c.a0 + c.a1*z + c.a2*pow(z, 2) + 
            c.a3*pow(z, 3) + c.a4*pow(z, 4))


def projection_factor(size_x = 512, proj_area = 512):
    """
    Relation between area projeted (in km) and 
    image size (in pixels)
    """
    return proj_area / size_x


def projection_area(i, j, half_x, half_y, attrs, alt_ag):

    Re = attrs.earth_radius
    alpha = projection_factor()
    arg = pow(half_x - i, 2) + pow(j - half_y, 2)

    return  (np.sqrt(arg) * alpha) / (Re + alt_ag)


def elevation_angle(a, attrs, alt_ag):
    """Elevation angle which an observer see the layer structure"""
    Re = attrs.earth_radius
    H = attrs.alt_obs
    
    return np.arctan2((Re + alt_ag) * np.sin(a), 
                      (Re + alt_ag) * np.cos(a) - (Re + H))


def azimuth_angle(i, j, half_x, half_y):
    """Anzimuth angle for each point (i, j) of image"""
    
    azimuth = np.arctan2(half_x - i, j - half_y) #verificar com Cristiano
    if azimuth < 0:
        azimuth += 2 * np.pi 
    return azimuth


def make_mapping(original, fname):
    
    
    attrs = get_attributes(fname)
    
    rot = attrs.rotation
    alt_ag = c.emission_band(imager_fname(fname).emission)
            
    size_x, size_y = original.shape[:]
    half_x = (size_x - 1) / 2  
    half_y = (size_y - 1) / 2
    
    az = np.zeros((size_x, size_y))
    a = np.zeros((size_x, size_y))
    ze = np.zeros((size_x, size_y))
    lf = np.zeros((size_x, size_y))
    
    imgmap = np.zeros((2, size_x, size_y), dtype=np.int16)
    
    
    for i in range(size_x):
        for j in range(size_y):
            
            az[i, j] = azimuth_angle(i, j, half_x, half_y)
            
            a[i, j] = projection_area(i, j, half_x, half_y, attrs, alt_ag)
            
            ze[i, j] = elevation_angle(a[i, j], attrs, alt_ag)
            
            lf[i, j] = lens_function(ze[i, j], attrs)
    
            imgmap[0, i, j] = attrs.xm - lf[i, j] * np.sin(az[i, j] - rot)
            imgmap[1, i ,j] = attrs.ym + lf[i, j] * np.cos(az[i, j] - rot)

    return imgmap



def linearization(fname, 
                  horizontal_flip = True):
    
    
    original = io.imread(fname, as_gray = True)
    
    mapping = make_mapping(original, fname)
    
    _, size_x, size_y = mapping.shape
    
    map_x = mapping[0, 0: size_x - 1, 0: size_y - 1]
    map_y = mapping[1, 0: size_x - 1, 0: size_y - 1]
    
    new_img = original[map_x, map_y] 
    
    if horizontal_flip:
        
        new_img = np.flipud(new_img)
    
    return new_img




def main():
    fname = "database/examples/OH_CA_20181112_002024.tif" 
    

    linearized = linearization(fname)
    
    
