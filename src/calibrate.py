import datetime as dt
import os
import json 
import pandas as pd
import sys
os.path.dirname(sys.executable)
from pathlib import Path

def remove_values(list_to_remove: list, 
                  item_to_remove:str = "") -> list:
    """Remove value in list"""
    return [item.strip() for item in list_to_remove if item != ""]

def get_date_from_folder(folder: str) -> dt.date:
    """split filename arguments and get calibration date"""
    args = folder.split(".")
    year = int(args[0])
    doy = int(args[1])
    
    return dt.date(year, 1, 1) + dt.timedelta(doy - 1)


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
    def result(self) -> dict:
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
    def data(self) -> pd.DataFrame:
        """Return calibrate data from stars"""
        header = remove_values(self.cal_section[0].split("  "))
    
        body = [i.split() for i in self.cal_section[1:-1]]
        return  pd.DataFrame(body, columns = header)




def run_for_all_files(
        site: str = "CA", 
        save: bool = True
        ) -> dict:
    
    """Get path with all times calibration 
    and append to one single dictionary"""
    infile = os.path.join(
        os.getcwd(), 
        "calibrate", 
        site
        )
        
    out_dict = {}
    
    for folder in os.listdir(infile):
        dat = load(infile, folder)
        date = get_date_from_folder(folder)
        out_dict.update({str(date): dat.result})
        
    if save:
        with open(os.path.join(infile, f"{site}.json"), 'w') as f:
            json.dump(out_dict, f)

    return out_dict


def get_calibration(
        time: dt.datetime, 
        site: str = "CA"
        ) -> dict:
    """Open json file for the last calibration for the time"""
    try:
        infile = os.path.join(os.getcwd(), 
                              "calibrate", 
                              site,
                              f"{site}.json")
        
        dat = json.load(open(infile))
    except:
        infile = os.path.join(os.getcwd(), 
                              "imager",
                              "calibrate", 
                              site,
                              f"{site}.json")
        
        dat = json.load(open(infile))

    ts = pd.to_datetime(list(dat.keys()))

    for num in range(len(ts) - 1):
        
        dt1 = pd.Timestamp(ts[num])
        dt2 = pd.Timestamp(ts[num + 1])
        
        if (dt1 > time) and (dt2 < time):
            return dat[str(dt2.date())]
        
        elif (time > max(ts)):
            return dat[str(max(ts).date())]

def main():
    site = "CA"
    df = run_for_all_files(site)
   
site = 'CA'   
infile = os.path.join(os.getcwd(), 
                      "imager",
                      "calibrate", 
                      site,
                      f"{site}.json")

dat = json.load(open(infile))

dat