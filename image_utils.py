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
        self.datetime = datetime.datetime.strptime(date + " " + time, '%Y%m%d %H%M%S')
  
    @property
    def time(self):
        return self.datetime.strftime("%H:%M:%S UT")
    
    @property
    def date(self):
        return self.datetime.strftime("%d/%m/%Y")

def doy_str_format(date: int) -> str:
    """Convert integer to string. Ex: 1 to 001"""
    
    if isinstance(date, datetime.datetime):
        doy = date.timetuple().tm_yday
    else:
        doy = date
    
    if doy < 10:
        str_doy = f"0{doy}"
    else:
        str_doy = f"{doy}"
        
    return  str_doy