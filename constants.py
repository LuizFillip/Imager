

class constants(object):
    
    # radius_equator, radius_polo (in km)
    equator_radius = 6378.14
    polo_radius = 6356.755
    
    @staticmethod
    def projection_area(proj: int = 2) -> int:
        
        """
        Projection area values in pixels
        """
        areas = {1: 256, 
                 2: 512, 
                 3: 1024, 
                 4: 2048}
        
        return areas[proj]

    @staticmethod
    def emission_band(band: str = "OH") -> int:
        
        """
        Altitude of emission layer (in km) 
        OH = IR-87
        """
        altitudes = {"OH": 87, 
                     "O2": 89, 
                     "Na": 94,
                     "O5": 96, 
                     "O6": 250}
        
        return altitudes[band]
    
    @staticmethod
    def sites():
        return 
    
    
def main():
    c = constants()
    
    print(c.emission_band())
    print(c.projection_area())
    
