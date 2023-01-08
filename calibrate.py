import datetime
import os
import json 
import pandas as pd
from image_utils import date_from_doy, remove_values
import sys
os.path.dirname(sys.executable)
from pathlib import Path


def get_date_from_folder(folder: str) -> datetime.date:
    """split filename arguments and get calibration date"""
    args = folder.split(".")
    year = int(args[0])
    doy = int(args[1])
    
    return datetime.date(year, 1, 1) + datetime.timedelta(doy - 1)



def get_calibration(time: datetime.datetime, 
                    site:str = "CA") -> dict:
    """Open json file for the last calibration for the time"""
    
    infile = os.path.join(str(Path.cwd()), "calibrate")
    dat = json.load(open(os.path.join(infile, site, f"{site}.json")))

    ts = pd.to_datetime(list(dat.keys()))
    
    for num in range(len(ts) - 1):
        
        dt1 = ts[num].date()
        dt2 = ts[num + 1].date()
        if (dt1 > time) and (dt2 < time):
            return dat[str(dt2)]
        
        elif (time > max(ts)):
            return dat[str(max(ts).date())]
        


class load(object):
    
    def __init__(self, infile, folder):
        
        path_of_folder = os.path.join(infile, folder)
        
        filename = [fi for fi in next(os.walk(path_of_folder))[-1] 
                    if fi.endswith(".dat")][0]
        
        
        dat = open(os.path.join(path_of_folder, filename), 
                   encoding = 'latin-1').read()

        sec = dat.find("Nr.")
        
        self.cal_section = dat[sec:].split("\n")
        self.dat_section = dat[:sec].split("\n")
        
        
    @property
    def result(self):
        """Return site parameters and lens functions result 
        and update into dictionary"""
        out_dict = {}
        for elem in self.dat_section:
            if "--" in elem:
                break
            elif elem == "":
                pass
            else:
                args = elem.split(": ")
                out_dict.update({args[0] : args[1].strip()})
        
        return out_dict
    
    @property
    def data(self):
        """Return calibrate data from stars"""
        header = remove_values(self.cal_section[0].split("  "))
    
        body = [i.split() for i in self.cal_section[1:-1]]
        return  pd.DataFrame(body, columns = header)



site = "CA"

def run_for_all_files(site: str = "CA", 
                      save: bool = True) -> dict:
    
    """Get path with all times calibration 
    and append to one single dictionary"""
    infile = os.path.join(str(Path.cwd()), 
                          "calibrate", 
                           site)
    
    _, folders, _ = next(os.walk(infile))
    
    
    out_dict = {}
    
    for folder in folders:
        dat = load(infile, folder)
        date = get_date_from_folder(folder)
        
        out_dict.update({str(date): dat.result})
        
        
    if save:
        with open(infile + site + ".json", 'w') as f:
            json.dump(out_dict, f)

    return out_dict


date = date_from_doy(2011, 264)


