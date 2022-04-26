from datetime import datetime
import os


def write_excep(excep, name_file, name_procc): # function for adding wrtite in an logfile
    now = datetime.now()
    if os.path.exists(name_file):
        with open(name_file, 'a') as o:
            o.write(f"{str(now)} -- {name_procc} -- {str(excep)} \n\n")
    else:
        with open(name_file, 'x') as o:
            o.write(f"{str(now)} -- {name_procc} -- {str(excep)} \n\n")