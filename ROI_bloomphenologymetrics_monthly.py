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
def check_for_bloominit(yearly_timeseries):
    arr = yearly_timeseries.values.copy()                   # avoid mutating the original list
    counting = []                      # keep track of True indexes, to count them later
    for i in range(len(arr)):          # cycle by index
        is_last = i + 1 >= len(arr)    # True if this is the last index in the array
        if arr[i] == True:
            counting.append(i)         # add value to list if True
        if is_last or arr[i] == False: # when we are at the last entry, or find a False
            if len(counting) < 2:      # check the length of our True indexes, and if less than 6
                for j in counting:
                    arr[j] = False     # make each False
            counting = []
    return arr
#%% Load your chlorophyll-a data file
os.chdir('C:\\Users\\afons\\OneDrive - Universidade de Lisboa\Documents\\artigos\\antarctic-peninsula-trends-2021\\resources\\cciv6data\\')
fh = np.load('chloc4so_19972022.npz', allow_pickle=True)
chl = fh['chl_oc4so'][:]
lat = fh['lat'][:]
lon = fh['lon'][:]
time = fh['time_date'][:] #time vector in datetime format
#%% Adjust time to monthly
chl_monthly = np.empty((len(lat), len(lon), 304)) #adjust according to monthly size
#size_test = pd.Series(data=chl[0, 0, :], index=time)
#len(size_test.resample('M').mean())
# Chl-a with daily means
for i in range(len(lat)):
    print(i)
    for j in range(len(lon)):
        pixel_ori = chl[i, j, :]
        # convert to pandas
        pixel_ori_pd = pd.Series(data=pixel_ori, index=time)
        # Average daily
        pixel_monthly = pixel_ori_pd.resample('M').mean()
        # Add to 3D array
        chl_monthly[i,j,:] = pixel_monthly
        if (i == 0) & (j == 0):
            time_monthly = pixel_monthly.index.values
#%% If you want to run a moving mean or interpolate, do it here
#%% Extract time from datetime
time_monthly_years = pd.to_datetime(time_monthly).year.values
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
            idx_year_chl = np.argwhere(time_monthly_years == yearchar).ravel()
            # create pandas
            chl_pixel = pd.Series(chl_monthly[i,j, :], index=time_monthly)
            # adapt timeseries to September - April of selected year
            sep_prevyear_arg = np.argwhere([(chl_pixel.index.month == 9) & (chl_pixel.index.year == yearchar-1)])[0][1]
            apr_year_arg = np.argwhere([(chl_pixel.index.month == 4) & (chl_pixel.index.year == yearchar)])[0][1]+1
            chl_pixel_sepapr = chl_pixel[sep_prevyear_arg:apr_year_arg]
            if chl_pixel_sepapr.count() == 0:
                continue
            # Use only the following two lines if you want to check a given seasonal cycle and where the threshold is
            #plt.plot(chl_pixel_sepapr)
            #plt.axhline(np.nanmedian(dfa_)*1.05)
            # calculate threshold (+5% above median)
            chl_pixel_abovethresh = chl_pixel_sepapr >= np.nanmedian(chl_pixel_sepapr)*1.05 #calculates treshold (+5% of the anual median)
            b_start = chl_pixel_abovethresh.index[np.argmax(check_for_bloominit(chl_pixel_abovethresh))].month
            b_term = chl_pixel_abovethresh.index[len(chl_pixel_abovethresh) - np.argmax(check_for_bloominit(chl_pixel_abovethresh[::-1])) - 1].month
            b_dur = b_term - b_start + 1
            bloom_peak = chl_pixel_sepapr.index[np.argmax(chl_pixel_sepapr)].month
            bloom_max = np.nanmax(chl_pixel_sepapr)
            bloom_mean = np.nanmean(chl_pixel_sepapr)
            total_production = integrate.simps(chl_pixel_sepapr.dropna().values.ravel()) #total area           
            bloom_amplitude = bloom_max - bloom_mean
            #save to matrices
            ROI_bloom_mean[i,j,k] = bloom_mean
            ROI_bloom_max[i,j,k] = bloom_max
            ROI_bloom_peak[i,j,k] = bloom_peak
            ROI_bloom_amplitude[i,j,k] = bloom_amplitude
            ROI_bloom_0[i,j,k] = b_start
            ROI_bloom_end[i,j,k] = b_term
            ROI_bloom_duration[i,j,k] = b_dur
            #ROI_bloom_num[i,j,k] = bloom_num
            ROI_total_production[i,j,k] = total_production
#%% Save to a pandas dataframe
roi_phenology = pd.DataFrame([ROI_bloom_mean,ROI_bloom_max,
                                        ROI_bloom_amplitude,ROI_bloom_peak,
                                        ROI_bloom_0, ROI_bloom_end,
                                        ROI_bloom_duration,
                                        ROI_total_production]).transpose()
#                                        ROI_bloom_num]).transpose()
roi_phenology_columns = ['Mean','Max','Amplitude','Bloom Peak Date','Bloom Start',
                               'Bloom End','Bloom Duration','Bloom Area',
                               'Total Production']#'Bloom Number']
roi_phenology.columns = roi_phenology_columns
# Save!
np.savez_compressed('phenologymetrics_usingmonthly',
                    ROI_phenology = roi_phenology)
# END OF THE SCRIPT #