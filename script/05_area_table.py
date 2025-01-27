# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 11:32:16 2025

@author: Viet Nguyen
"""

import rasterio
import numpy
import glob
import pandas as pd

# get predicted raster paths
rast_paths = glob.glob('01_output/03_pred_rast/*classified.tif')
rast_paths

# read predicted rasters
for path in rast_paths:
    with rasterio.open(path) as rast:
        print(rast.profile)
        # get data year
        year = path.split('\\')[1].split('_')[1]
        # read raster as array
        arr = rast.read()
        # create table of pixel counts
        df = pd.DataFrame(numpy.unique(arr, return_counts=True)).T
        df.rename(columns={1:f'{year}'}, inplace=True)
        globals()[f'data_{year}']=df
        
# join all year table as one
data = data_2020.merge(data_2021).merge(data_2022)
data = data.drop(0, axis='columns').drop(0)
# rename
data.rename(index={1:'Water',2:'Algae',3:'Juncus',4:'Typha',5:'Phragmites',
                   6:'Phalaris', 7:'Other wetland vegetation'}, inplace=True)
# convert pixel number to m2
data = data*2.5e-5
data = data.round(2)
# save
data.to_csv('01_output/07_spec_area.csv')
