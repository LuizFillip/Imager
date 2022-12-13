import datetime 
import os
import sys
os.path.dirname(sys.executable)


class imager_fname(object):
    
    """Convert filename attributes into datetime format"""
    
    def __init__(self, filename):
        
  
        infos = filename[:-4].split("_")
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
    
    
def get_files(infile, extension = ""): 
    _, _, files = next(os.walk(infile))
    
    return [f for f in files if f.endswith(extension)]


    
def filename_from_date(t:datetime.datetime, 
                       layer:str = "O6", 
                       site:str = "CA") -> str:
    """Convert All_Sky filename from site, layer and datetime"""
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
        
        
infile = "database/examples/OH_0179_20070707194753.tif"

convert_tif_to_png(infile)