#!/usr/bin/env python
# coding: utf-8

# In[33]:


'''
plotting the first contributed data
'''

# load modules
import numpy as np
import xarray as xr
import glob
import os

header = '/home/oie_storage/PRIVATE/DATA/'

# list the subfolders 
for name in glob.glob(header + '*/'):
    print(name)
# save the subfolders into a list
subfolders = [f.path for f in os.scandir(header) if f.is_dir() ]

# loop through each folder
# recall that a timeseries with integradted variable over an 
# area is saved as timeseries_*.nc and time series from the raw grid
# is saved as full_*.nc

ds = xr.open_dataset(subfolder + 'full_*.nc')



