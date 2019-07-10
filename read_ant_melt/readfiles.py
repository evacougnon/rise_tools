'''
    plotting the first contributed data
    mostly a testing purpose
    idea is to plot all the time serries for integrated
      melt rates (total ice and for different ice shelves
      assuming they divided their ice shelves using the 
      matlab tool from Chad Green

Created: June 2019
Author: Eva Cougnon
Last modif:

'''

################
# load modules
################
import numpy as np
import pandas as pd
import xarray as xr
import glob
import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

#header = '/home/oie_storage/PRIVATE/DATA/'
header = '/home/ecougnon/Documents/RISE_after_OIE/VM_backup/DATA/'

#################################
# Which ice shelf melt to plot! 
#################################
is_list = ['total_massloss', 'ronne_filchner', 'pig', 'thwaites', 'dotson', 'shackleton', 'totten_moscowuni', 'amery', 'ross']

######################
# list the subfolders 
######################
for name in glob.glob(header + '*/'):
    print(name)
# save the subfolders into a list
subfolders = [f.path for f in os.scandir(header) if f.is_dir() ]
model_name = ["" for ii in range(len(subfolders))]
for ii in range(0,len(subfolders)):
    model_name[ii] = os.path.basename(subfolders[ii])

###############################
# allocate memory
###############################
# integrated mass loss for each of the ice shelves
#time_vec = pd.date_range('1992','2019',freq='Y') # to use if datetime format wanted!
time_vec = np.arange(1992.,2019.)
# ice shelf mass loss
is_ml = xr.Dataset({is_list[0]:(('time','model'),np.zeros((len(time_vec), \
                                                           len(model_name))))}, \
                   coords = {'time':time_vec, 'model':model_name}, \
                   attrs = {'units': 'Gt/yr'})
for ii in range(1,len(is_list)):
    is_ml = is_ml.assign({is_list[ii]:(('time','model'), \
                          np.zeros((len(time_vec),len(model_name))))}) 
###########################    
# loop through each folder
# to save the mass loss
###########################
# naming recall that a timeseries with integradted variable over an 
# area is saved as timeseries_*.nc (timeselies_annual.nc when annually saved)
# and time series from the raw grid is saved as full_*.nc
for n in range(0,len(model_name)):
    if model_name[n] == 'tmp':
        print('- ignore tmp folder!')
    elif model_name[n] == 'coco':
        print('- COCO: so far we only have access to the time averaged and not the time series of the melt! cannot run this analysis on the COCO data')
    elif model_name[n] == 'roms-richter':
        print('- roms-richter: need to calculate the integrated melt! -- not yet included in the analysis! And includes only 1 year (2007)')
    else:
        print('- common folder: ' + model_name[n])
        ds = xr.open_dataset(header + model_name[n] + '/timeseries_annual.nc')
        # checking the right starting index for 1992
        # will need to readapt for models not starting from 1992
        # but depends what the majority of model use between year and a simple
        # integer or an actual datetime value!
        time_str_id = np.where(ds.time[0]==is_ml.time)
        time_end_id = np.where(ds.time[-1]==is_ml.time)
        for ii in range(0,len(is_list)):
            is_ml[is_list[ii]].values[time_str_id[0][0]:time_end_id[0][0]+1,n] = \
             is_ml[is_list[ii]].values[time_str_id[0][0]:time_end_id[0][0]+1,n] + \
             ds[is_list[ii]].values

# missing values should be nan! Change the exact value of 0.0 to nan:
is_ml.where(is_ml!=0.0)

###############################
# plotting
###############################
fontP = FontProperties()
fontP.set_size('small')
my_dpi = 300
plt.figure(figsize=(4000/my_dpi,3500/my_dpi))
plt.clf()    

for ii in range(0,len(is_list)):
    ax = plt.subplot(3,3,ii+1)
    for n in range(0,len(model_name)):
        is_ml[is_list[ii]][:,n].plot(marker = 'o', label=model_name[n])
    ax.set_xlim([time_vec[0], time_vec[-1]])
    ax.set_ylabel('Mass loss (Gt/yr)')
    ax.set_title(is_list[ii])

plt.legend(prop=fontP)
#plt.legend(loc='upper center', bbox_to_anchor=(-0.5, -0.05), \
#           fancybox=True,ncol=len(model_name))
plt.tight_layout()
plt.show()

