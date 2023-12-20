import numpy as np
import imager as im

class get_attributes:

    def __init__(self, fname):
        file_attrs = im.imager_fname(fname)
        time_file = file_attrs.datetime
        site_file = file_attrs.site
        dat = im.get_calibration(time_file, site = site_file)
        
        
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


def projection_factor(
        size_x = 512, 
        proj_area = 512
        ):
    """
    Relation between area projeted (in km) and 
    image size (in pixels)
    """
    return proj_area / size_x


def projection_area(i: int, 
                    j:int, 
                    half_x:int, 
                    half_y:int, attrs, alt_ag):
    """
    Compute the projection for each pixel in the image"""
    Re = im.constants().equator_radius
    alpha = projection_factor()
    arg = pow(half_x - i, 2) + pow(j - half_y, 2)

    return  (np.sqrt(arg) * alpha) / (Re + alt_ag)


def elevation_angle(a, attrs, alt_ag):
    
    """
    Elevation angle which an observer see the
    layer structure
    """
    Re = im.constants().equator_radius
    H = attrs.alt_obs
    
    return np.arctan2((Re + alt_ag) * np.sin(a), 
                      (Re + alt_ag) * np.cos(a) - 
                      (Re + H))


def azimuth_angle(i, j, half_x, half_y):
    """Anzimuth angle for each point (i, j) of image"""
    azimuth = np.arctan2(half_x - i, j - half_y) #verificar com Cristiano
    if azimuth < 0:
        azimuth += 2 * np.pi 
    return azimuth


    


