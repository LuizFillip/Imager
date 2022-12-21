import datetime
import os
import json 
import pandas as pd

import sys
os.path.dirname(sys.executable)
from pathlib import Path


def get_date_from_folder(folder: str) -> datetime.date:
    """split filename arguments and get calibration date"""
    args = folder.split(".")
    year = int(args[0])
    doy = int(args[1])
    
    return datetime.date(year, 1, 1) + datetime.timedelta(doy - 1)

def convert_infos_into_dict(absolute_path: str, folder: str) -> dict:
    """Read .dat files and update into dictionary"""
    filename = [fi for fi in next(os.walk(absolute_path + folder))[-1] 
            if fi.endswith(".dat")][0]
    
    with open(f"{absolute_path}{folder}/{filename}", 
              encoding='latin-1') as f:
        
        dat = [line.strip() for line in f.readlines()]
    
    out_dict = {}
    for elem in dat:
        if "--" in elem:
            break
        elif elem == "":
            pass
        else:
            args = elem.split(": ")
            out_dict.update({args[0] : args[1].strip()})
            
    return out_dict
        

def calibration_infos_by_date(infile: str, folder: str) -> dict:
    """Create an dictonary with date of calibration"""
    date = get_date_from_folder(folder)
    
    return {str(date): convert_infos_into_dict(infile, 
                                               folder)}

def run_for_all_files(infile: str)-> dict:
    """Get path with all times calibration and append to one single dictionary"""
    _, folders, _ = next(os.walk(infile))

    out_dict = {}

    for folder in folders:

        out_dict.update(calibration_infos_by_date(infile, 
                                                  folder))

    return out_dict



def save_json(infile: str, name: str = "cariri.json") -> None:
    """Save results"""
    with open(infile + "cariri.json", 'w') as f:
        json.dump(run_for_all_files(infile), f)
        
        

def get_calibration(time: datetime.datetime, 
                     filename:str = "CA.json") -> dict:
    """Open json file for the last calibration for the time"""
    
    infile = os.path.join(str(Path.cwd()), "calibracao")
    dat = json.load(open(os.path.join(infile, filename)))

    dates = pd.to_datetime(list(dat.keys()))
    
    for num in range(len(dates) - 1):
        
        if (dates[num] > time) and (dates[num + 1] < time):
            return dat[str(dates[num + 1].date())]
        
        elif (time > max(dates)):
            return dat[str(max(dates).date())]
        
