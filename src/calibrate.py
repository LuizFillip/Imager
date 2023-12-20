import datetime as dt
import os
import json 
import pandas as pd


def remove_values(list_to_remove: list, 
                  item_to_remove: str = "") -> list:
    """Remove value in list"""
    return [item.strip() for item in list_to_remove if item != ""]

def date_from_folder(folder: str) -> dt.date:
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
        site: str = "CA"
        ) -> dict:
    
    """Get path with all times calibration 
    and append to one single dictionary"""
    infile = os.path.join(
        os.getcwd(), 
        'imager',
        "calibrate", 
        site
        )
        
    out_dict = {}
    
    for folder in os.listdir(infile):
        dat = load(infile, folder)
        date = date_from_folder(folder)
        out_dict.update({str(date): dat.result})
        

    with open(os.path.join(infile, f"{site}.json"), 'w') as f:
        json.dump(out_dict, f)

    return out_dict



def attributes_img(path):
    
    filename = os.path.split(path)[-1]
    
    infos = filename[:-4].split("_")
    
    datetime = dt.datetime.strptime(
        infos[2] + " " + infos[-1], 
        '%Y%m%d %H%M%S')
    
    return {'dn': datetime, 'site': infos[1], 'layer': infos[0]}
  
def load_dat(site):

    infile = os.path.join(
            os.getcwd(), 
            "imager",
            "calibrate", 
            site,
            f"{site}.json"
            )
  
    return json.load(open(infile))


def get_calibration(file) -> dict:
    """
    Open json file for the last 
    calibration for the time
    """
    
    attrs = attributes_img(file)
    site = attrs['site']
    dn = attrs['dn']
    
    df = load_dat(site)

    ts = pd.to_datetime(list(df.keys()))

    for num in range(len(ts) - 1):
        
        start = ts[num]
        ending = pd.Timestamp(ts[num + 1])
        
        if (start > dn) and (ending < dn):
            return df[str(ending.date())]
        
        elif (dn > max(ts)):
            return df[str(max(ts).date())]



# get_calibration(file)
