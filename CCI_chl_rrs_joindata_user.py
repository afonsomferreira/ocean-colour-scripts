# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:53:48 2020

Joins different datafiles downloaded with "CCI_chl_download...py" scripts along the temporal dimension of the dataset.

Note that this script should only be used after using the CCI_chl_download scripts. Else, make sure the data is stored
in .npz files and that the name of the variables match.

@author: ambferreira
"""
import os
import sys
import glob
import numpy as np
def join_datafiles(file_directory):
    """Joins 3D CCI chl + rrs datafiles created using the CCI_chl_download_user.py script
    along the time dimension"""
    file_names = glob.glob1(file_dir, "*.npz")
    ### Confirm datafiles
    print('This directory has ' + str(len(file_names)) + ' .npz data files.')
    check_dir = input('Do you want to proceed and start joining them? [Y/N]')
    if check_dir != 'Y':
        sys.exit("ERROR: Please repeat")
    for i in file_names:
        print(i)
        file_temp = np.load(i, allow_pickle=True)
        chl_temp = np.float16(file_temp['chl'])
        Rrs555_temp = np.float16(file_temp['Rrs_555'])
        Rrs510_temp = np.float16(file_temp['Rrs_510'])
        Rrs490_temp = np.float16(file_temp['Rrs_490'])
        Rrs443_temp = np.float16(file_temp['Rrs_443'])        
        time_temp = file_temp['time']
        time_date_temp = file_temp['time_date']
        if i == file_names[0]:
            chl = chl_temp
            Rrs_443 = Rrs443_temp
            Rrs_490 = Rrs490_temp
            Rrs_510 = Rrs510_temp
            Rrs_555 = Rrs555_temp
            lat = file_temp['lat']
            lon = file_temp['lon']
            time = time_temp
            time_date = time_date_temp
        else:
            chl = np.dstack((chl, chl_temp))
            Rrs_443 = np.dstack((Rrs_443, Rrs443_temp))
            Rrs_490 = np.dstack((Rrs_490, Rrs490_temp))
            Rrs_510 = np.dstack((Rrs_510, Rrs510_temp))
            Rrs_555 = np.dstack((Rrs_555, Rrs555_temp))
            time = np.hstack((time, time_temp))
            time_date = np.hstack((time_date, time_date_temp))
        del(file_temp, chl_temp, time_temp, time_date_temp)
    return chl, Rrs_443, Rrs_490, Rrs_510, Rrs_555, lat, lon, time, time_date
### Asks user for data directory
print('Please store datafiles that you wish to join in a single folder with no other .npz files')
print('Please make sure the files are in the correct alphabetical and temporal order')
# C:\\Users\PhytoTroph\Documents\Artigos\NA_Anomaly_2009\datasets\datafiles_chl_2009
#file_dir = input("Please enter the directory where your datafiles are located:")
file_dir = 'C:\\Users\\afons\\Documents\\artigos\\socean\\resources\\chl\\cci42\\'
os.chdir(file_dir)
### Loads and joins every file
chl, Rrs_443, Rrs_490, Rrs_510, Rrs_555, lat, lon, time, time_date = join_datafiles(file_dir)
### Save as a unique file
np.savez_compressed('cci_chlrrsv42_19982019', lat=lat, lon=lon, chl=chl,
                    Rrs_443=Rrs_443, Rrs_490=Rrs_490, Rrs_510=Rrs_510,
                    Rrs_555=Rrs_555,time=time, time_date=time_date)
print('Done!')
