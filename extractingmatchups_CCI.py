# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 18:46:52 2020

@author: PhytoTroph
"""

import os
import numpy as np
import netCDF4 as nc4
import pandas as pd
import datetime as datetime
#%%
# Import insitu data
os.chdir('C:\\Users\\afons\\Downloads')
insitudata = pd.read_csv('insitudata_example.csv', sep=';') # Load matchups file.
insitu_year = np.array(insitudata['Year'].values)
insitu_month = np.array(insitudata['Month'].values)
insitu_day = np.array(insitudata['Day'].values)
insitu_hour = np.array(insitudata['Hour'].values)
insitu_minute = np.array(insitudata['Minute'].values)
insitu_second = np.array(insitudata['Second'].values)
insitu_lat = np.array(insitudata['Latitude'].values)
insitu_lon = np.array(insitudata['Longitude'].values)
insitu_chl = np.array(insitudata['Chla'].values)
# Convert insitu sample date to datetime format
insitu_datetime = np.empty(len(insitu_year), dtype=object)
for i in range(0, len(insitu_datetime)):
    insitu_datetime[i] = datetime.datetime(year = int(insitu_year[i]),
                                           month = int(insitu_month[i]),
                                           day = int(insitu_day[i]),
                                           hour = int(insitu_hour[i]),
                                           minute = int(insitu_minute[i]),
                                           second = int(insitu_second[i]))
# Convert insitu datetime to match server time (in this case CCI time, which uses days after 1970-1-1)
insitu_servertime = np.empty([len(insitu_lat)])
start = datetime.datetime(1970,1,1,0,0) # Adapt to server initial date
for i in range(0,len(insitu_servertime)):
    timedelta_servertime = insitu_datetime[i]-start # calculates days and seconds from initial date
    insitu_dayssince = timedelta_servertime.days # in our case, just the days are needed
    insitu_servertime[i] = insitu_dayssince
#%% Select requisites of the matchups
# Spatial requisites (choose the one which applies)
boxsize = 3 # find matchups within 3x3 pixels
# boxsize = 5 if you want 5x5 box
# Temporal requisites
matchup_timedelta = datetime.timedelta(days=1) # find matchups +-1 day (minimum CCI)

# matchup_timedelta = datetime.timedelta(hours=3) if you prefer +-3 hours
#%% Pre-allocate matchup array (where no matchups are found = NaN)
matchup_chl = np.empty(len(insitu_lat))*np.nan
#%% Start searching for matchups
#Import latitude, longitude and time data from CCI server
nc_in = nc4.Dataset('https://www.oceancolour.org/thredds/dodsC/CCI_ALL-v6.0-DAILY') #open connection
# Load server latitude and longitude
lati = nc_in.variables['lat'][:]
loni = nc_in.variables['lon'][:]
# Load time data
sat_time = nc_in.variables['time'][:]
for i in range(0,len(matchup_chl)): # loop along each insitu sample
    print(i)
    ## Find pixel closest to our in-situ location
    lat_index = np.argmin(abs(lati-insitu_lat[i]))
    lon_index = np.argmin(abs(loni-insitu_lon[i]))
    ## Check temporal matchup
    # Create maximum and minimum timedelta (+-1 day in this case)
    time_upperboundary = insitu_datetime[i] + datetime.timedelta(days=1)
    time_lowerboundary = insitu_datetime[i] - datetime.timedelta(days=1)
    # Convert boundaries to server time (days since 1970-01-01 in this cases)
    start = datetime.datetime(1970,1,1,0,0)
    time_upperboundary_delta = time_upperboundary-start # calculates days and seconds from initial date
    time_upperboundary_server = time_upperboundary_delta.days # in our case, just the days are needed
    time_lowerboundary_delta = time_lowerboundary-start # calculates days and seconds from initial date
    time_lowerboundary_server = time_lowerboundary_delta.days # in our case, just the days are needed    
    # Get timesteps within your boundaries
    matchup_time = np.argwhere((sat_time > time_lowerboundary_server) & (sat_time < time_upperboundary_server))
    matchup_time = matchup_time[0][0] # make sure to keep only the indices
    if np.nansum(matchup_time) == 0:
        continue    # if there are no images within your time boundaries, continue loop
    # Check spatial matchup
    if boxsize == 3:
        matchup_raw = np.array(nc_in.variables['chlor_a'][matchup_time, lat_index-1:lat_index+2, lon_index-1:lon_index+2])
        matchup_raw[matchup_raw == 9.96921e+36] = np.nan
        if np.nansum(matchup_raw) == 0:
            continue    # if all pixels are NaN, continue (you can add more restrictions here)
        else:
            matchup_valid = matchup_raw[~np.isnan(matchup_raw)]
            matchup_chl[i] = np.nanmean(matchup_valid)
            print('NEW MATCH-UP')
    elif boxsize == 5:
        matchup_raw = np.array(nc_in.variables['chlor_a'][matchup_time, lat_index-2:lat_index+3, lon_index-2:lon_index+3])
        matchup_raw[matchup_raw == 9.96921e+36] = np.nan
        if np.nansum(matchup_raw) == 0:
            continue    # if all pixels are NaN, continue (you can add more restrictions here)
        else:
            matchup_valid = matchup_raw[~np.isnan(matchup_raw)]
            matchup_chl[i] = np.nanmean(matchup_valid)
            print('NEW MATCH-UP')
    # to increase boxsize, just add and subtract to the latitude/longitude indices
# Save everything to a pandas dataframe
matchup_dataframe = pd.DataFrame([insitu_datetime, insitu_year, insitu_month,
                                       insitu_day, insitu_hour, insitu_minute,
                                       insitu_second, insitu_lat, insitu_lon,
                                       insitu_chl, matchup_chl])
matchup_dataframe = matchup_dataframe.transpose()
matchup_dataframe.columns = ['Date', 'Year', 'Month', 'Day', 'Hour',
                                  'Minute', 'Second', 'Latitude', 'Longitude',
                                  'Chla_insitu', 'Chla_satellite']
# Change directory to where you would like to save your file (if needed)
#os.chdir('C:\\Users\\Afonso\\Documents\\Trabalho\\Artigos\\Tom\matchups')
# Save as csv
matchup_dataframe.to_csv('matchups_fulllist.csv',index=False)
# Keep and save only valid matchups (remove all NaNs)
matchup_dataframe = matchup_dataframe[matchup_dataframe['Chla_satellite'].notna()]
matchup_dataframe.to_csv('matchups_onlyvalid.csv',index=False)

