import datetime 


class imager_fname(object):
    
    """Convert filename attributes into datetime format"""
    
    def __init__(self, filename):
        
        if ".tif" in filename:
            infos = filename.replace(".tif", "").split("_")
        else:
            infos = filename.replace(".png", "").split("_")

        date = infos[2]
        time = infos[-1]
        self.emission = infos[0]
        self.site = infos[1]
        self.datetime = datetime.datetime.strptime(date + " " + time, '%Y%m%d %H%M%S')
  
    @property
    def time(self):
        return self.datetime.strftime("%H:%M:%S UT")
    
    @property
    def date(self):
        return self.datetime.strftime("%d/%m/%Y")
    
def filename_from_date(t:datetime.datetime, 
                       layer:str = "O6", 
                       site:str = "CA") -> str:
    """Convert All_Sky filename from site, layer and datetime"""
    return f'{layer}_{site}_{t.strftime("%Y%m%d_%H%M%S")}'