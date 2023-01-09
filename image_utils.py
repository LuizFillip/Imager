import datetime 
import os
import typing as T
import pandas as pd


class imager_fname(object):
    
    """Get datetime from filename (EMBRACE format)"""
    
    def __init__(self, filename):
        
        filename = os.path.split(filename)[-1]
  
        infos = filename[:-4].split("_")
        date = infos[2]
        time = infos[-1]
        self.emission = infos[0]
        self.site = infos[1]
        self.datetime = datetime.datetime.strptime(date + " " + time, 
                                                   '%Y%m%d %H%M%S')
  
    @property
    def str_time(self):
        return self.datetime.strftime("%H:%M:%S UT")
    
    @property
    def str_date(self):
        return self.datetime.strftime("%d/%m/%Y")
    
    
    
def get_files(infile: T.TextIO, extension = ".tif"): 
    """
    get all files in directory like glob

    Parameters
    ----------
    infile : TYPE
        DESCRIPTION.
    extension : TYPE, optional
        DESCRIPTION. The default is ".tif".

    Returns
    -------
    list
        DESCRIPTION.

    """
    _, _, files = next(os.walk(infile))
    
    return [f for f in files if f.endswith(extension)]

def date_from_doy(year: int, doy:int) -> datetime.datetime:
    """Return date from year and doy"""
    return pd.Timestamp(datetime.date(year, 1, 1) + datetime.timedelta(doy - 1))


def remove_values(list_to_remove: list, 
                  item_to_remove:str = "") -> list:
    """Remove value in list"""
    return [item.strip() for item in list_to_remove if item != ""]


def filename_from_date(t: datetime.datetime, 
                       layer:str = "O6", 
                       site:str = "CA") -> str:
    """Create EMBRACE filename format from site, layer and datetime"""
    return f'{layer}_{site}_{t.strftime("%Y%m%d_%H%M%S")}'


def convert_tif_to_png(filename, path = ""):
    """Convert to PNG"""
    if path == "":
        src = os.path.join(path, filename)
        dest = os.path.join(path, filename.replace(".tif",'.png') )     
        
    else:
        src = filename
        dest = filename.replace(".tif",'.png')
    try:
        os.rename(src, dest)   
    except RuntimeError:
        print("All files was converted")
        
        