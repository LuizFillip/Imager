import numpy as np 


def make_mapping(
        fname, 
        altitude_of_emission = 87, 
        projection = 512
        ):
    
    
    attrs = get_attributes(fname)
    
    rot = attrs.rotation
    alt_ag = altitude_of_emission
            
    half_x = (projection - 1) / 2  
    half_y = (projection - 1) / 2
    
    az = np.zeros((projection, projection))
    a = np.zeros((projection, projection))
    ze = np.zeros((projection, projection))
    lf = np.zeros((projection, projection))
    
    imgmap = np.zeros(
        (2, 
        projection, 
        projection), 
        dtype = np.int16
        )
 
    
    for i in range(projection):
        for j in range(projection):
            
            az[i, j] = azimuth_angle(
                i, j, half_x, half_y)
            
            a[i, j] = projection_area(
                i, j, half_x, half_y, attrs, alt_ag)
            
            ze[i, j] = elevation_angle(
                a[i, j], attrs, alt_ag)
            
            lf[i, j] = lens_function(
                ze[i, j], attrs)
    
            imgmap[0, i, j] = attrs.xm - lf[i, j] * np.sin(az[i, j] - rot)
            imgmap[1, i ,j] = attrs.ym + lf[i, j] * np.cos(az[i, j] - rot)

    return imgmap



def save_maps():
    
    import xarray as xr
    
    fname = "database/examples/OH_CA_20181112_002024.tif" 


    def make_maps_in_all_altitudes(fname):
    
        altitudes = im.constants.emission_band(values = True)
        
        return [make_mapping(fname, altitude_of_emission = alt) 
                 for alt in altitudes]  
        
    

def linearization(
        fname, 
        mapping, 
        horizontal_flip = True
        ):
    
    
    original = io.imread(
        fname, as_gray = True)
    
    _, size_x, size_y = mapping.shape
    
    # verificar esses indices com cristiano
    map_x = mapping[0, 0: size_x, 0: size_y]
    map_y = mapping[1, 0: size_x, 0: size_y]
    
    new_img = original[map_x, map_y] 
    
    if horizontal_flip:
        
        new_img = np.flipud(new_img)
    
    return new_img