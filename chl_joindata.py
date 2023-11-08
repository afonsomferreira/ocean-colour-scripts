# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:53:48 2020

Joins different datafiles downloaded with "CCI_chl_download...py" scripts along the temporal dimension of the dataset.

@author: ambferreira
"""
import os
import glob
import numpy as np
from netCDF4 import Dataset
### Define File directory where the images are stored ###
# Images must have equal size for all axes (lat x lon x time) #
file_dir = 'C:\\Users\\afons\\Documents\\artigos\\bia\\areas_aquimar\\resources\\area_e\\'
os.chdir(file_dir)
file_names = glob.glob1(file_dir, "*.npz")
# Use this one if data is in netcdf, else it assumes data is stored in numpy zipped archive (.npz)
#file_names = glob.glob1(file_dir, "*.nc")
for i in file_names:
    print(i)
    # Use these lines if data is in netcdf
    #fh = Dataset(i, mode='r')
    #chl_temp = fh.variables['chl'][:]
    #time_temp = fh.variables['time'][:]
    #time_date_temp = fh.variables['time_date'][:]
    file_temp = np.load(i, allow_pickle=True)
    chl_temp = np.array(file_temp['chl'][:])
    time_temp = file_temp['time']
    time_date_temp = file_temp['time_date']
    if i == file_names[0]:
        chl = chl_temp
        lat = np.array(file_temp['lat'])
        lon = np.array(file_temp['lon'])
        time = time_temp
        time_date = time_date_temp
    else:
        chl = np.dstack((chl, chl_temp))
        time = np.hstack((time, time_temp))
        time_date = np.hstack((time_date, time_date_temp))
    del(file_temp, chl_temp, time_temp, time_date_temp)
### Loads and joins every file
### Save as a unique file
np.savez_compressed('chl1km_areae_19982020', lat=lat, lon=lon, chl=chl,
                    time=time, time_date=time_date)
