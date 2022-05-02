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
    """Joins 3D CCI chl datafiles created using the CCI_chl_download_user.py script
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
        chl_temp = np.float64(file_temp['chl'])
        chl_temp = chl_temp[:,:,:-1]
        time_temp = file_temp['time'][:-1]
        time_date_temp = file_temp['time_date'][:-1]
        if i == file_names[0]:
            chl = chl_temp
            lat = file_temp['lat']
            lon = file_temp['lon']
            time = time_temp
            time_date = time_date_temp
        else:
            chl = np.dstack((chl, chl_temp))
            time = np.hstack((time, time_temp))
            time_date = np.hstack((time_date, time_date_temp))
        del(file_temp, chl_temp, time_temp, time_date_temp)
    return chl, lat, lon, time, time_date
### Asks user for data directory
print('Please store datafiles that you wish to join in a single folder with no other .npz files')
print('Please make sure the files are in the correct alphabetical and temporal order')
# C:\\Users\PhytoTroph\Documents\Artigos\NA_Anomaly_2009\datasets\datafiles_chl_2009
#file_dir = input("Please enter the directory where your datafiles are located:")
file_dir = 'C:\\Users\\afons\\Documents\\artigos\\coccos-chase-2021\\resources\\chl\\19982020'
os.chdir(file_dir)
### Loads and joins every file
chl, lat, lon, time, time_date = join_datafiles(file_dir)
### Save as a unique file
np.savez_compressed('chl_amt19982020', lat=lat, lon=lon, chl=chl,
                    time=time, time_date=time_date)
print('Done!')
