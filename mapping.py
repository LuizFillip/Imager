import matplotlib.pyplot as plt
import numpy as np
from calibrate import get_calibration
from image_utils import imager_fname
from constants import constants as c



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
        
    

    
def lens_function(z: float, c: float) -> float:
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


def projection_area(i: int, 
                    j:int, 
                    half_x:int, 
                    half_y:int, attrs, alt_ag):
    """Compute the projection for each pixel in the image"""
    Re = c().equator_radius
    alpha = projection_factor()
    arg = pow(half_x - i, 2) + pow(j - half_y, 2)

    return  (np.sqrt(arg) * alpha) / (Re + alt_ag)


def elevation_angle(a, attrs, alt_ag):
    """Elevation angle which an observer see the layer structure"""
    Re = c().equator_radius
    H = attrs.alt_obs
    
    return np.arctan2((Re + alt_ag) * np.sin(a), 
                      (Re + alt_ag) * np.cos(a) - (Re + H))


def azimuth_angle(i, j, half_x, half_y):
    """Anzimuth angle for each point (i, j) of image"""
    azimuth = np.arctan2(half_x - i, j - half_y) #verificar com Cristiano
    if azimuth < 0:
        azimuth += 2 * np.pi 
    return azimuth


def make_mapping(fname, 
                 altitude_of_emission = 87, 
                 projection = 512):
    
    
    attrs = get_attributes(fname)
    
    rot = attrs.rotation
    alt_ag = altitude_of_emission
            
    #size_x, size_y = original.shape[:]
    half_x = (projection - 1) / 2  
    half_y = (projection - 1) / 2
    
    az = np.zeros((projection, projection))
    a = np.zeros((projection, projection))
    ze = np.zeros((projection, projection))
    lf = np.zeros((projection, projection))
    
    imgmap = np.zeros((2, 
                       projection, 
                       projection), 
                       dtype = np.int16)
    
    
    for i in range(projection):
        for j in range(projection):
            
            az[i, j] = azimuth_angle(i, j, half_x, half_y)
            
            a[i, j] = projection_area(i, j, half_x, half_y, attrs, alt_ag)
            
            ze[i, j] = elevation_angle(a[i, j], attrs, alt_ag)
            
            lf[i, j] = lens_function(ze[i, j], attrs)
    
            imgmap[0, i, j] = attrs.xm - lf[i, j] * np.sin(az[i, j] - rot)
            imgmap[1, i ,j] = attrs.ym + lf[i, j] * np.cos(az[i, j] - rot)

    return imgmap










def main():
    fname = "database/examples/OH_CA_20181112_002024.tif" 
    
    
    #mapping = make_mapping(fname)
    
    #print(c().emission_band())
    
    



main()    
    
