import datetime as dt
import os
import typing as T
import pandas as pd



def fn2datetime(filename):

    infos = filename[:-4].split("_") 
    date_time = infos[2] + " " + infos[-1]
    form = '%Y%m%d %H%M%S'
    return dt.datetime.strptime(date_time, form)
      

class imager_fname(object):
    
    """Get datetime from filename (EMBRACE format)"""
    
    def __init__(self, filename):
        
        filename = os.path.split(filename)[-1]
  
        infos = filename[:-4].split("_")
        date = infos[2]
        time = infos[-1]
        self.emission = infos[0]
        self.site = infos[1]
        self.datetime = dt.datetime.strptime(
            date + " " + time, 
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
    """
    
    return [f for f in os.listdir(infile) if 
            f.endswith(extension)]

def date_from_doy(year: int, doy:int) -> dt.datetime:
    """Return date from year and doy"""
    return pd.Timestamp(
        dt.date(year, 1, 1) +  dt.timedelta(doy - 1))


def folder_from_date(dn, site = 'CA'):
    return dn.strftime(f'{site}_%Y_%m%d')


def filename_from_date(
        dn: dt.datetime, 
        layer:str = "O6", 
        site:str = "CA"
        ) -> str:
    
    """
    Create EMBRACE filename format from site,
    layer and datetime
    """
    return dn.strftime(f'{layer}_{site}_%Y%m%d_%H%M%S')


def convert_tif_to_png(filename, path = None):
    """Convert to PNG"""
    if path is not None:
        src = os.path.join(path, filename)
        dest = os.path.join(path, filename.replace(".tif",'.png') )     
        
    else:
        src = filename
        dest = filename.replace(".tif",'.png')
    try:
        os.rename(src, dest)   
    except RuntimeError:
        print("All files was converted")
 
    
# dn = dt.datetime(2013, 1, 14, 20)
# folder_from_date(dn, site = 'CA')