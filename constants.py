import numpy as np

class constants(object):
    
    def __init__(self):
    # radius_equator, radius_polo (in km)
        self.equator_radius = 6378.14
        self.polo_radius = 6356.755
    

    def earth_radius(self, lat_obs):
        """
        Compute earth radius from a latitude
        """
        eq = self.equator_radius
        ep = self.polo_radius
        
        num = pow(eq * ep, 2)
        den = (pow(eq * np.sin(lat_obs), 2) + 
               pow(ep * np.cos(lat_obs), 2.0))
        
        return np.sqrt(num / den)
    
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
    def emission_band(band: str = "OH",
                      keys = False, 
                      items = False, 
                      values = False) -> int:
        
        """
        Altitude of emission layer (in km) 
        OH (Hydroxilia) = IR-87
        """
        band_alts = {"OH": 87, 
                     "O2": 89, 
                     "Na": 94,
                     "O5": 96, 
                     "O6": 250}
        
        if keys:
            return list(band_alts.keys())
        elif values:
            return list(band_alts.values())
        elif items:
            return list(band_alts.items())
        else:
            return band_alts[band]
    
    @staticmethod
    def sites(site_name:str = "CA") -> tuple:
        """
        Get EMBRACE stations coordinates (longitude, latitude)
        and your full name
        """
        coords = {"BJL": (-43.546917, -13.256378), 
                  "BV": (-60.710941, 2.870188),
                  "CA": (-36.528307, -7.381122), 
                  "CP": (-45.009307, -22.703813), 
                  "SMS": (-53.821934, -29.442348), 
                  "CF": (-58.404019, -62.090483)}
        
        names = {"BJL": "Bom Jesus da Lapa", 
                  "BV": "Boa Vista",
                  "CA": "Sao Joao do Cariri", 
                  "CP": "Cachoeira Paulista", 
                  "SMS": "Sao Martinho da Serra", 
                  "CF": "Comandante Ferraz"}
        
        return names[site_name], coords[site_name]
    
    
def main():
    c = constants()
    
    print(c.emission_band(values = True))
    #print(c.equator_radius)
    
main()