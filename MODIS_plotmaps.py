# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 18:26:58 2023

EXERCISE 3

Plotting chlorophyll-a maps: in depth

MAKE SURE THE DATAFILES AND SCRIPTS ARE ALL ON THE SAME DIRECTORY

@author: afons
"""
import os #change folders,
import numpy as np # perform calculations and basic math,
import matplotlib.pyplot as plt # plot data
import matplotlib.ticker as mticker
import pandas as pd # work with dataframes,tables, spreadsheets, etc.,
import netCDF4 as nc4 # work with netcdf files, the standard file for satellite 2D and 3D data,
import cartopy #work with geographical projections and maps"
from scipy import stats #calculate statistics
import matplotlib as mpl
import xarray as xr
# Change to your working directory where datafiles and scripts are stored
os.chdir('C:\\Users\\afons\\Downloads\\rafa_operantar2024\\modis\\')
#%% Part 1 - Load MODIS .nc image
file_path = 'AQUA_MODIS.20240101_20240108.L3m.8D.CHL.chlor_a.4km.NRT.nc'
# Load the NetCDF file using xarray
ds = xr.open_dataset(file_path)
# Access the variables
chl = np.array(ds['chlor_a'])
lat = np.array(ds['lat'])
lon = np.array(ds['lon'])
#%% Subset by latitude
chl_subset = chl[(lat <= -55) & (lat >= -70), :]
chl_subset = chl_subset[: , (lon >= -70) & (lon <= -50)]
lat_subset = lat[(lat <= -55) & (lat >= -70)]
lon_subset = lon[(lon >= -70) & (lon <= -50)]
#%% Plot figure
plt.figure()
map = plt.axes(projection=cartopy.crs.AzimuthalEquidistant(central_longitude=-60, central_latitude=-62))
map.set_extent([-67, -53, -67, -60])
f1 = map.pcolormesh(lon_subset, lat_subset, chl_subset[:-1, :-1], transform=cartopy.crs.PlateCarree(), shading='flat',
                    cmap=plt.cm.turbo, norm=mpl.colors.LogNorm(vmin=0.1, vmax=5))
gl = map.gridlines(draw_labels=True, alpha=0.5, linestyle='dotted', color='black')
cbar = plt.colorbar(f1, fraction=0.04, pad=0.1)
cbar.set_label('Chl-$\it{a}$ (mg.m$^{-3}$)', fontsize=14)
map.coastlines(resolution='10m', color='black', linewidth=1)
#map.add_feature(cartopy.feature.NaturalEarthFeature('physical', 'land', '50m',
#                                        edgecolor='k',
#                                        facecolor=cartopy.feature.COLORS['land']))
plt.tight_layout()
graphs_dir = 'C:\\Users\\afons\\Downloads\\rafa_operantar2024\\modis\\AQUA_MODIS.20240101_20240108.png'
plt.savefig(graphs_dir,format = 'png', bbox_inches = 'tight', dpi = 300)
plt.close()
#%% Repeat for other image
file_path = 'AQUA_MODIS.20240109_20240116.L3m.8D.CHL.chlor_a.4km.NRT.nc'
# Load the NetCDF file using xarray
ds = xr.open_dataset(file_path)
# Access the variables
chl = np.array(ds['chlor_a'])
lat = np.array(ds['lat'])
lon = np.array(ds['lon'])
#%% Subset by latitude
chl_subset = chl[(lat <= -55) & (lat >= -70), :]
chl_subset = chl_subset[: , (lon >= -70) & (lon <= -50)]
lat_subset = lat[(lat <= -55) & (lat >= -70)]
lon_subset = lon[(lon >= -70) & (lon <= -50)]
#%% Plot figure
plt.figure()
map = plt.axes(projection=cartopy.crs.AzimuthalEquidistant(central_longitude=-60, central_latitude=-62))
map.set_extent([-67, -53, -67, -60])
f1 = map.pcolormesh(lon_subset, lat_subset, chl_subset[:-1, :-1], transform=cartopy.crs.PlateCarree(), shading='flat',
                    cmap=plt.cm.turbo, norm=mpl.colors.LogNorm(vmin=0.1, vmax=5))
gl = map.gridlines(draw_labels=True, alpha=0.5, linestyle='dotted', color='black')
cbar = plt.colorbar(f1, fraction=0.04, pad=0.1)
cbar.set_label('Chl-$\it{a}$ (mg.m$^{-3}$)', fontsize=14)
map.coastlines(resolution='10m', color='black', linewidth=1)
#map.add_feature(cartopy.feature.NaturalEarthFeature('physical', 'land', '50m',
#                                        edgecolor='k',
#                                        facecolor=cartopy.feature.COLORS['land']))
plt.tight_layout()
graphs_dir = 'C:\\Users\\afons\\Downloads\\rafa_operantar2024\\modis\\AQUA_MODIS.20240109_20240116.png'
plt.savefig(graphs_dir,format = 'png', bbox_inches = 'tight', dpi = 300)
plt.close()
#%% Repeat for other image
file_path = 'AQUA_MODIS.20240117_20240124.L3m.8D.CHL.chlor_a.4km.NRT.nc'
# Load the NetCDF file using xarray
ds = xr.open_dataset(file_path)
# Access the variables
chl = np.array(ds['chlor_a'])
lat = np.array(ds['lat'])
lon = np.array(ds['lon'])
#%% Subset by latitude
chl_subset = chl[(lat <= -55) & (lat >= -70), :]
chl_subset = chl_subset[: , (lon >= -70) & (lon <= -50)]
lat_subset = lat[(lat <= -55) & (lat >= -70)]
lon_subset = lon[(lon >= -70) & (lon <= -50)]
#%% Plot figure
plt.figure()
map = plt.axes(projection=cartopy.crs.AzimuthalEquidistant(central_longitude=-60, central_latitude=-62))
map.set_extent([-67, -53, -67, -60])
f1 = map.pcolormesh(lon_subset, lat_subset, chl_subset[:-1, :-1], transform=cartopy.crs.PlateCarree(), shading='flat',
                    cmap=plt.cm.turbo, norm=mpl.colors.LogNorm(vmin=0.1, vmax=5))
gl = map.gridlines(draw_labels=True, alpha=0.5, linestyle='dotted', color='black')
cbar = plt.colorbar(f1, fraction=0.04, pad=0.1)
#cbar.ax.set_yticklabels(['0.1', '0.5', '1', '3', '10'], fontsize=14)
cbar.set_label('Chl-$\it{a}$ (mg.m$^{-3}$)', fontsize=14)
map.coastlines(resolution='10m', color='black', linewidth=1)
#map.add_feature(cartopy.feature.NaturalEarthFeature('physical', 'land', '50m',
#                                        edgecolor='k',
#                                        facecolor=cartopy.feature.COLORS['land']))
plt.tight_layout()
graphs_dir = 'C:\\Users\\afons\\Downloads\\rafa_operantar2024\\modis\\AQUA_MODIS.20240117_20240124.png'
plt.savefig(graphs_dir,format = 'png', bbox_inches = 'tight', dpi = 300)
plt.close()
