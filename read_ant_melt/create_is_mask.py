########################################################
#
# create masks for each ice shelves, following the boundaries
# from the antbounds toolbox from Chad Greene:
# Antarctic boundaries, grounding line, and masks from InSAR
# https://au.mathworks.com/matlabcentral/fileexchange/60246-antarctic-boundaries-grounding-line-and-masks-from-insar
#
# initially this script was made to process roms-richter model data
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
import scipy.io as sio # can read maltab file

'''
#############
# optimising
##############
from dask.distributed import Client
c = Client()
c
'''

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
shelves_coord_path = os.path.join(os.pardir,'matlab_tools','shelves.mat')
shelf_masks_dict = os.path.join(data_dir,'POST_PROCESS','shelf_mask.npy')
#########################
# Load data
#########################
grd = xr.open_dataset(grd_path)

##############################
# Create masks for each shelf
# can take long: run once and save the dictionary
##############################

from scipy.spatial import KDTree #kd-tree for quick nearest-neighbor lookup

#def make_mask_ice_shelves(shelves_coord_path, grd):
    # find nearest neighbours of ant_bounds lat_lon coords on the roms grid 
    # and define ice shelf masks and middle coordinates
    # copy/pasted from Ole's GitHub (see link at the top of the script
shelves = {}

    # read in ice shelf coordinates derived from ant_bounds matlab package
coords = sio.loadmat(shelves_coord_path)['shelves'][0].squeeze()

for idx in range(np.size(coords)):
    name = coords[idx][0][0]
    shelves[name]={}
    shelves[name]['lat']= coords[idx][1].squeeze()
    shelves[name]['lon']= coords[idx][2].squeeze()

lat_flat = grd.lat_rho.stack(etaxi = ('eta_rho','xi_rho'))
lon_flat = grd.lon_rho.stack(etaxi = ('eta_rho','xi_rho'))
points = np.column_stack((lat_flat.values,lon_flat.values))
tree = KDTree(points)

for idx in range(np.size(coords)):
    name = coords[idx][0][0]
    lats = shelves[name]['lat']
    lons = shelves[name]['lon']

    target = np.column_stack((lats,lons))
    k_query = 113 # The number of nearest neighbors to return in the following command
    # tip: use a relativelly large k_query to unsure the difference of resolution
    # does not omit point on the ice shelf, mask from the grd file should mask
    # the extra points
    dist, ind = tree.query(target,k=k_query)
    if ind.shape != (0,k_query):
        eta = lat_flat[np.unique(ind)].eta_rho.values
        xi = lat_flat[np.unique(ind)].xi_rho.values
        shelves[name]['eta'] = eta
        shelves[name]['xi'] = xi

        mask_tmp = np.zeros_like(grd.mask_rho.values)
        mask_tmp[eta,xi] = 1
        mask_tmp[grd.zice.values == 0.0] = 0
        mask_tmp[grd.mask_rho.values == 0.0] = 0
        mask_tmp = (mask_tmp == 1)
        shelves[name]['mask']=mask_tmp

np.save(shelf_masks_dict,shelves)







