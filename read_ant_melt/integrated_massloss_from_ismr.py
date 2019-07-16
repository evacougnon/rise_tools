########################################################
#
# calculate the integrated mass loss (Gt/yr) from the 
# ice shelf melt rate on the raw grid.
# Later may include the area-averaged melt rate for each
# ice shelf but now, not sure it's really needed!
#
# initially made to process roms-richter model data
# shared as time-average (1 year simulation -- 2007)
# melt rate (m/yr) for each grid point
#
# should be easy to apply to other models -- if too hard
# move this file to roms-richter data folder and create
# a new script for each of the models when needed
#
# script highly inspired by Ole Richter's github scripts:
# https://github.com/kuechenrole/antarctic_melting/blob/master/notebooks/analysis/mass_loss_analysis.ipynb
#
# Author: Eva Cougnon
# Created: July 2019
# last modif:
#
###########################################################

################
# load modules
################
import xarray as xr
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import pandas as pd


#########################
# Choose model to analyse
# with grid file
#########################
model_name = 'roms-richter'
grd_name = 'waom2_grd.nc'

#############################
# paths to useful directories
#############################
data_dir = os.path.join(os.pardir,os.pardir,'DATA',model_name)
grd_path = os.path.join(data_dir,'GRD',grd_name)
mr_path = os.path.join(data_dir,'full_annual_m_2007.nc') # will need to update when multiple files!!....
shelf_masks_dict = os.path.join(data_dir,'POST_PROCESS','shelf_mask.npy')
save_path = os.path.join(data_dir,'POST_PROCESS','timeseries_annual.nc')

#########################
# Load data
#########################
grd = xr.open_dataset(grd_path)
mr = xr.open_dataset(mr_path).m.squeeze()
mr = mr.where((grd.mask_rho ==1) & (grd.zice<0.0))
shelves = np.load(shelf_masks_dict)[()] # load as a dictionary!
#time_vec = mr.ocean_time # ideally! however wrong date in roms-richter
time_vec = np.arange(2007,2008)

# useful numbers! -- may change between models!
s2a = 3600*24*365.25
rhoi = 916
mask_vostock = (grd.lat_rho<-75) & (grd.lat_rho>-80) & \
               (grd.lon_rho>95) & (grd.lon_rho<115)
mr = mr.where((mask_vostock == 0))
mr = mr*s2a # change from m/s to m/yr
mask_is = (grd.mask_rho==1) & (grd.zice < 0.0) # mask to get all ice shelves
dA = (1/(grd.pm*grd.pn)).where(mask_is)
ismr2bml = dA*rhoi*(10**-12)

#################################
# Which ice shelf melt to plot! 
# tried to keep the same spelling than the naming 
# system in antbounds toolbox
#################################
is_list = ['Total_massloss', 'Abbot', 'Amery', 'Dotson', 'Getz', 'LarsenC', 'LarsenD', 'Mertz', 'Pine Island', 'Ross', 'Ronne_filchner', 'Shackleton', 'Thwaites', 'Totten_moscowuni']

###############################
# allocate memory
###############################
# integrated basal mass loss for each of the ice shelves
# and area-averaged of the basal melt rate
is_bml = xr.Dataset({is_list[0]:(('time'),np.zeros((len(time_vec))))}, \
                    coords = {'time':time_vec}, attrs = {'units': 'Gt/yr'})
#is_bmr = xr.Dataset({is_list[0]:(('time'),np.zeros((len(time_vec))))}, \
#                    coords = {'time':time_vec}, attrs = {'units': 'm/yr'})
for ii in range(1,len(is_list)):
    is_bml = is_bml.assign({is_list[ii]:(('time'), np.zeros((len(time_vec))))})
#    is_bmr = is_bmr.assign({is_list[ii]:(('time'), np.zeros((len(time_vec))))})

###########################################
# ice shelf melt rate (area-averaged) and 
# ice shelf mass loss integrated) for 
# each ice shelf
############################################
for name in is_list:
    if name == 'Total_massloss':
        is_bml[name].values[0] = (mr*ismr2bml).stack(loc=['eta_rho', 'xi_rho']) \
                                              .sum(dim='loc')
    elif name == 'Abbot':
        is_bml[name].values[0] = (mr.where((shelves['Abbot']['mask']==1) | \
                                           (shelves['Abbot 1']['mask']==1) | \
                                           (shelves['Abbot 2']['mask']==1) | \
                                           (shelves['Abbot 3']['mask']==1) | \
                                           (shelves['Abbot 4']['mask']==1) | \
                                           (shelves['Abbot 5']['mask']==1) | \
                                           (shelves['Abbot 6']['mask']==1)) \
                                  * ismr2bml) \
                                 .stack(loc=['eta_rho', 'xi_rho']) \
                                 .sum(dim='loc')
    elif name == 'Getz':
        is_bml[name].values[0] = (mr.where((shelves['Getz']['mask']==1) | \
                                           (shelves['Getz 1']['mask']==1) | \
                                           (shelves['Getz 2']['mask']==1)) \
                                  * ismr2bml) \
                                 .stack(loc=['eta_rho', 'xi_rho']) \
                                 .sum(dim='loc')
    elif name == 'LarsenD':
        is_bml[name].values[0] = (mr.where((shelves['LarsenD']['mask']==1) | \
                                           (shelves['LarsenD 1']['mask']==1)) \
                                  * ismr2bml) \
                                 .stack(loc=['eta_rho', 'xi_rho']) \
                                 .sum(dim='loc')
    elif name == 'Ross':
        is_bml[name].values[0] = (mr.where((shelves['Ross East']['mask']==1) | \
                                           (shelves['Ross West']['mask']==1)) \
                                  * ismr2bml) \
                                 .stack(loc=['eta_rho', 'xi_rho']) \
                                 .sum(dim='loc')
    elif name == 'Ronne_filchner':
        is_bml[name].values[0] = (mr.where((shelves['Ronne']['mask']==1) | \
                                           (shelves['Filchner']['mask']==1)) \
                                  * ismr2bml) \
                                 .stack(loc=['eta_rho', 'xi_rho']) \
                                 .sum(dim='loc')
    elif name == 'Totten_moscowuni':
        is_bml[name].values[0] = (mr.where((shelves['Totten']['mask']==1) | \
                                           (shelves['Moscow University']['mask']==1)) \
                                  * ismr2bml) \
                                 .stack(loc=['eta_rho', 'xi_rho']) \
                                 .sum(dim='loc')
    else:
        is_bml[name].values[0] = (mr.where((shelves[name]['mask']==1)) \
                                  * ismr2bml) \
                                 .stack(loc=['eta_rho', 'xi_rho']) \
                                 .sum(dim='loc')

#########################################
# saving!
#########################################
is_bml.to_netcdf(save_path)





