# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 10:26:52 2019
This script calculates phenology indices for each pixel
@author: Afonso Ferreira
"""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.path import Path
from scipy import integrate
def serial_date_to_string(srl_no):
    new_date = datetime.datetime(1970,1,1,0,0) + datetime.timedelta(hours = srl_no)
    return new_date
def start_stop(a, trigger_val):
    """"FINDS INDICES OF START AND END OF BLOOMS"""
    # "Enclose" mask with sentients to catch shifts later on
    mask = np.r_[False, np.equal(a, trigger_val), False]
    # Get the shifting indices
    idx = np.flatnonzero(mask[1:] != mask[:-1])
    # Get the start and end indices with slicing along the shifting ones
    return zip(idx[::2], idx[1::2]-1)
#%% Load your chlorophyll-a data file
os.chdir('C:\\Users\\afons\\OneDrive - Universidade de Lisboa\Documents\\artigos\\antarctic-peninsula-trends-2021\\resources\\cciv6data\\')
fh = np.load('chloc4so_19972022.npz', allow_pickle=True)
chl = fh['chl_oc4so'][:]
lat = fh['lat'][:]
lon = fh['lon'][:]
time = fh['time_date'][:] #time vector in datetime format
#%% Adjust time to daily
chl_daily = np.empty((len(lat), len(lon), 9238))
# Chl-a with daily means
for i in range(len(lat)):
    print(i)
    for j in range(len(lon)):
        pixel_ori = chl[i, j, :]
        # convert to pandas
        pixel_ori_pd = pd.Series(data=pixel_ori, index=time)
        # Average daily
        pixel_daily = pixel_ori_pd.resample('D').mean()
        # Add to 3D array
        chl_daily[i,j,:] = pixel_daily
        if (i == 0) & (j == 0):
            time_daily = pixel_daily.index.values
#%% If you want to run a moving mean or interpolate, do it here
#%% Extract time from datetime
time_daily_years = pd.to_datetime(time_daily).year.values
#%% Pre-allocate phenology indices
ROI_bloom_mean = np.empty((len(lat), len(lon), 24))*np.nan
ROI_bloom_max = np.empty((len(lat), len(lon), 24))*np.nan
ROI_bloom_peak = np.empty((len(lat), len(lon), 24))*np.nan
ROI_bloom_amplitude = np.empty((len(lat), len(lon), 24))*np.nan
ROI_bloom_0 = np.empty((len(lat), len(lon), 24))*np.nan
ROI_bloom_end = np.empty((len(lat), len(lon), 24))*np.nan
ROI_bloom_duration = np.empty((len(lat), len(lon), 24))*np.nan
ROI_bloom_area = np.empty((len(lat), len(lon), 24))*np.nan
ROI_bloom_num = np.empty((len(lat), len(lon), 24))*np.nan
ROI_total_production = np.empty((len(lat), len(lon), 24))*np.nan
# Loop goes through each pixel and year and calculates bloom phenology metrics
for i in range(len(lat)):
    print(i)
    for j in range(len(lon)):
        for k, yearchar in enumerate(range(1999, 2023)):
            # consider excluding the first and last year of the dataset
            idx_year_chl = np.argwhere(time_daily_years == yearchar).ravel()
            # create pandas
            chl_pixel = pd.Series(chl_daily[i,j, :], index=time_daily)
            # adapt timeseries to September - April of selected year
            s=""
            sep_prevyear = s.join((str(yearchar-1), '-09-01'))
            sep_prevyear_arg = np.argwhere(chl_pixel.index == sep_prevyear)[0][0]
            apr_year = s.join((str(yearchar), '-04-30'))
            apr_year_arg = np.argwhere(chl_pixel.index == apr_year)[0][0]+1
            chl_pixel_sepapr = chl_pixel[sep_prevyear_arg:apr_year_arg]
            if chl_pixel_sepapr.count() == 0:
                continue
            # Use only the following two lines if you want to check a given seasonal cycle and where the threshold is
            #plt.plot(dfa_)
            #plt.axhline(np.nanmedian(dfa_)*1.05)
            # calculate threshold (+5% above median)
            chl_pixel_abovethresh = chl_pixel_sepapr >= np.nanmedian(chl_pixel_sepapr)*1.05 #calculates treshold (+5% of the anual median)
            mask_tresh = chl_pixel_abovethresh.values
            blooms_ind = pd.DataFrame(start_stop(mask_tresh.ravel(), trigger_val=True))  #identify periods above threshold (blooms)
            blooms_dur = blooms_ind.values[:, 1]-blooms_ind.values[:, 0] # For each bloom, calculates duration
            blooms_dur[blooms_dur < 15] = 0 # checks if blooms have duration below 15 days and excludes them
            blooms_ind = blooms_ind.values[np.argwhere(blooms_dur > 0).ravel()]
            max_index = chl_pixel_sepapr.idxmax()
            for k, item in enumerate(blooms_ind):
                if chl_pixel_sepapr.index[item[0]] <= max_index < chl_pixel_sepapr.index[item[1]]: # checks if the bloom includes the yearly maximum. Otherwise, it is not the main bloom of the year and the algorithm moves on
                    b_start = chl_pixel_sepapr.index[item[0]].dayofyear #calculates bloom initiation day of the year
                    b_end = chl_pixel_sepapr.index[item[1]].dayofyear #calculates bloom termination day of the year
                    if b_end < b_start: #checks if bloom day of the year is laters than the start (may occur for late year blooms)
                        b_duration = 365-b_start+b_end
                    else:
                        b_duration = b_end-b_start # calculates bloom duration
            bloom_num = len(blooms_ind) # calculate number of blooms in the year
            bloom_max = chl_pixel_sepapr.max(skipna=True)[0] # maximum chl-a in the year (bloom peak)
            bloom_mean = chl_pixel_sepapr.mean(skipna=True)[0] # yearly mean chl-a
            bloom_peak = max_index.dayofyear # day of bloom peak
            total_production = integrate.simps(chl_pixel_sepapr.dropna().values.ravel())/chl_pixel_sepapr.count() #total area           
            bloom_amplitude = bloom_max - bloom_mean
            #save to matrices
            ROI_bloom_mean[i,j,k] = bloom_mean
            ROI_bloom_max[i,j,k] = bloom_max
            ROI_bloom_peak[i,j,k] = bloom_peak
            ROI_bloom_amplitude[i,j,k] = bloom_amplitude
            ROI_bloom_0[i,j,k] = b_start
            ROI_bloom_end[i,j,k] = b_end
            ROI_bloom_duration[i,j,k] = b_duration
            ROI_bloom_num[i,j,k] = bloom_num
            ROI_total_production[i,j,k] = total_production
#%% Save to a pandas dataframe
roi_phenology = pd.DataFrame([ROI_bloom_mean,ROI_bloom_max,
                                        ROI_bloom_amplitude,ROI_bloom_peak,
                                        ROI_bloom_0, ROI_bloom_end,
                                        ROI_bloom_duration,
                                        ROI_total_production,
                                        ROI_bloom_num]).transpose()
roi_phenology_columns = ['Mean','Max','Amplitude','Bloom Peak Date','Bloom Start',
                               'Bloom End','Bloom Duration','Bloom Area',
                               'Total Production','Bloom Number']
roi_phenology.columns = roi_phenology_columns
# Save!
np.savez_compressed('phenologymetrics_usingdaily',
                    ROI_phenology = roi_phenology)
# END OF THE SCRIPT #