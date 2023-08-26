import datetime as dt
import os
import typing as T
import pandas as pd



    
    
    
def get_files(infile: T.TextIO, extension = ".tif"): 
    """
    get all files in directory like glob
    """
    _, _, files = next(os.walk(infile))
    
    return [f for f in files if f.endswith(extension)]

def date_from_doy(year: int, doy:int) -> dt.datetime:
    """Return date from year and doy"""
    return pd.Timestamp(dt.date(year, 1, 1) +
                        dt.timedelta(doy - 1))



def filename_from_date(
        t: dt.datetime, 
        layer:str = "O6", 
        site:str = "CA"
        ) -> str:
    """Create EMBRACE filename format from site, layer and datetime"""
    return f'{layer}_{site}_{t.strftime("%Y%m%d_%H%M%S")}'


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
        
path_in = "database/AllSky/2023/"

def run_in_path(path_in):

    _, _, files = next(os.walk(path_in))
    
    for filename in files:
        
        convert_tif_to_png(filename, path = path_in)
        