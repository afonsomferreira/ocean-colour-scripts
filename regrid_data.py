# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 15:49:19 2019

@author: PhytoTroph
"""

import numpy as np
import scipy.interpolate
import os
import matplotlib
matplotlib.rcParams.update({'errorbar.capsize': 0})
import matplotlib.pyplot as plt
## Load data that you want to regrid
os.chdir('C:\\Users\\Afonso\\Documents\\Trabalho\\Artigos\\chlanomaly-2009-2021\\resources\\datasets\\datafiles_chl_2009')
chl_file = np.load('CCI_chl_v5_updated.npz', allow_pickle=True)
chl = chl_file['chl'][:,:,:] #only february 1 to march 31
lati = chl_file['lat'][:]
loni = chl_file['lon'][:]
time = chl_file['time_date'][:]
### Load new grid (from a lower resolution product) or create new grid
os.chdir('C:\\Users\\Afonso\\Documents\\Trabalho\\Artigos\\chlanomaly-2009-2021\\resources\\datasets\\ssh_currents')
filedata = np.load('hycomncoda_processeddata.npz')
lat = filedata['lat']
lon = filedata['lon']
filedata.close()
### Create mesh using latitude/longitude for both grid
X, Y = np.meshgrid(loni, lati)
XI, YI = np.meshgrid(lon,lat)
### Pre-allocate new regridded matrix
chl_regridded = np.empty((138, 126, len(time)))
### Regrid original dataset to new grid (lower resolution)
for i in range(0, len(time)):
    chl_regridded[:,:,i] = scipy.interpolate.griddata((X.flatten(),Y.flatten()),chl[:,:,i].flatten() , (XI,YI),method='linear')
### Test (make sure lat/lon is ok when plotting)
plt.pcolormesh(lon, lat, np.log10(chl_regridded[:,:,i]), cmap=plt.cm.jet)
### Save
np.savez_compressed('CCIchl_regriddedtoHYCOM',chl=chl_regridded, lat=lat, lon=lon, time=time)
