

class constants(object):
    
    # radius_equator, radius_polo (in km)
    equator_radius = 6378.14
    polo_radius = 6356.755
    
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
    def emission_band(band:str = "OH") -> int:
        
        """
        Altitude of emission layer (in km) 
        OH = IR-87
        """
        altitude_values = {"O5": 96, 
                           "O6": 250, 
                           "OH": 87, 
                           "O2": 89, 
                           "NaD": 94}
        
        return altitude_values[band]
    
    
def main():
    c = constants()
    
    print(c.emission_band())
    print(c.projection_area())
    
