

class constants(object):
    
    # radius_equator, radius_polo (in km)
    equator_radius, polo_radius = 6378.14, 6356.755
    
    
    @staticmethod
    def projection_area(proj_area: str = 2) -> int:
        
        """
        Projection area values 
        """
        areap_values = {1: 256, 
                        2: 512, 
                        3: 1024, 
                        4: 2048}
        
        return areap_values[proj_area]

    @staticmethod
    def emission_band(band:str = "OH_IR-87") -> int:
        
        """
        Altitude of emission layer (in km) 
        """
        altitude_values = {"OI_557.7": 96, 
                           "OI_630.0": 250, 
                           "OH_IR-87": 87, 
                           "O2_(0-1)": 89, 
                           "NaD": 94}
        
        return altitude_values[band]
    
    
def main():
    c = constants()
    
    print(c.emission_band())
    print(c.projection_area())
    
