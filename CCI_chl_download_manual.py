# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 14:47:00 2020

Downloads chlorophyll a 3D (latitude x longitude x time) dataset from the Ocean Colour - Climate Change Initiave (OC-CCI) using OPENDAP.

Please note that this is the manual version of this script. If you do not feel comfortable writing Python code, check the user input version of this script.

Only works for the OC-CCI v5 daily dataset with 4km resolution (most recent). Future versions will allow downloading older datasets.

@author: ambferreira
"""

import os
import datetime
from pathlib import Path
import numpy as np
import netCDF4 as nc4
def serial_date_to_string(srl_no):
    """Converts CCI serial number time to datetime"""
    new_date = datetime.datetime(1970, 1, 1, 0, 0) + datetime.timedelta(srl_no - 1)
    return new_date
def define_ROI(lat_upper, lat_lower, lon_upper, lon_lower):
    """Defines Region of Interest latitude and longitude to download"""
    try:
        lat_upper = int(lat_upper)
        lat_lower = int(lat_lower)
        lon_upper = int(lon_upper)
        lon_lower = int(lon_lower)
    except ValueError:
        print("ERROR: Please enter correct latitude/longitude")
    LATBD = [lat_upper, lat_upper]
    LONBD = [lon_lower, lon_upper]
    print('Your region of interest is:')
    print('Latitude:', LATBD)
    print('Longitude:', LONBD)
    return LATBD, LONBD
def define_time(time_init, time_final):
    """Defines period of time of interest to download"""
    try:
        time_start_year = int(time_init[0:4])
        time_start_month = int(time_init[5:7])
        time_start_day = int(time_init[8:10])
    except ValueError:
        print("ERROR: Please enter correct initial date")
    try:
        time_end_year = int(time_final[0:4])
        time_end_month = int(time_final[5:7])
        time_end_day = int(time_final[8:10])
    except ValueError:
        print("ERROR: Please enter correct final date")
    time_start_datetime = datetime.datetime(time_start_year, time_start_month, time_start_day)
    time_end_datetime = datetime.datetime(time_end_year, time_end_month, time_end_day)
    time_diff = (time_end_datetime-time_start_datetime).days
    print('Your data timespan is:')
    print('Initial date:', time_start)
    print('Final date:', time_end)
    print('That corresponds to', time_diff, 'days.')
    return time_start_datetime, time_end_datetime
def download_cci(lat_boundaries, lon_boundaries, time_init_date, time_final_date):
    """Downloads chl data from CCI v5 4km using previously defined
    Region of Interest and Time Period by user"""
    # Open netcdf4 file using OPENDAP
    nc_in = nc4.Dataset('https://www.oceancolour.org/thredds/dodsC/CCI_ALL-v5.0-DAILY')
    # Extract latitude and longitude
    lati = nc_in.variables['lat'][:]
    loni = nc_in.variables['lon'][:]
    lat_lb = np.argmin(abs(lati-lat_boundaries[0])) #sets latitude lower boundary
    lat_ub = np.argmin(abs(lati-lat_boundaries[1])) #sets latitude upper boundary
    lon_lb = np.argmin(abs(loni-lon_boundaries[0])) #sets longitude lower boundary
    lon_ub = np.argmin(abs(loni-lon_boundaries[1])) #sets longitude lower boundary
    lon = np.array(nc_in.variables['lon'][lon_lb:lon_ub])
    lat = np.array(nc_in.variables['lat'][lat_lb:lat_ub])
    # Extract time
    time_total = np.array(nc_in.variables['time'][:])
    time_total_date = np.empty(len(time_total), dtype=np.object)
    for i, item in enumerate(time_total):
        time_total_date[i] = serial_date_to_string(int(time_total[i]))
    time_start_ind = np.where(time_total_date == time_init_date)[0][0]
    time_start_end = np.where(time_total_date == time_final_date)[0][0]+1
    time_array = np.array(nc_in.variables['time'][time_start_ind:time_start_end])
    time_array_date = np.empty(len(time_array), dtype=np.object)
    for i, item in enumerate(time_array):
        time_array_date[i] = serial_date_to_string(int(time_array[i]))
    chl = np.array(nc_in.variables['chlor_a'][time_start_ind:time_start_end,
                                              lat_lb:lat_ub, lon_lb:lon_ub])
    # Swaps axes to lon, lat, time
    chl = np.swapaxes(np.swapaxes(chl, 0, 2), 0, 1)
    # Replaces invalid values with NaNs
    chl[chl == 9.96921E36] = np.nan
    return chl, lat, lon, time_array, time_array_date
### Define ROI
#Please enter upper right corner latitude [-90-90°N]:
lat_max = 'XX'
#Please enter lower left corner latitude [-90-90°N]:
lat_min = 'XX'
#Please enter upper right corner longitude [-180-180°E]:
lon_max = 'XX'
#Please enter lower left corner longitude [-180-180°E]:
lon_min = 'XX'
LATBD, LONBD = define_ROI(lat_max, lat_min, lon_max, lon_min)
### Define timespan
# Please enter initial day [YYYY-MM-DD]:
time_start = 'YYYY-MM-DD'
# Please enter final day [YYYY-MM-DD]:
time_end = 'YYYY-MM-DD'
time_start_datetime, time_end_datetime = define_time(time_start, time_end)
### Download data
#Please enter the desired name for the downloaded file
filename_out_chl = 'cci_chl_download'
chl, lat, lon, time_array, time_array_date = download_cci(LATBD,
                                                          LONBD,
                                                          time_start_datetime,
                                                          time_end_datetime)
### Save data in Downloads Folder by default
os.chdir(str(Path.home() / "Downloads"))
np.savez_compressed(filename_out_chl, lat=lat, lon=lon, chl=chl,
                    time=time_array, time_date=time_array_date)
