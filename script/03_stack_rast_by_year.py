# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 17:25:51 2024

@author: Viet Nguyen
"""

import os
import glob
import rasterio

# check wd
os.getcwd()
os.chdir(os.getcwd().replace('\\script', ''))
os.getcwd()


# get preprocessd raster directory (clip and aggregate in 1.1)
prep_rast_dir = '01_output/01_prep_rast/'

# get preprocessed raster paths by year
rast_2020_paths = glob.glob(f'{prep_rast_dir}/2020*.tif')
rast_2020_paths
rast_2021_paths = glob.glob(f'{prep_rast_dir}/2021*.tif')
rast_2021_paths
rast_2022_paths = glob.glob(f'{prep_rast_dir}/2022*.tif')
rast_2022_paths
rast_paths = [rast_2020_paths, rast_2021_paths, rast_2022_paths]
rast_paths

for rast_year_path in rast_paths:
    year = rast_year_path[0].split('\\')[1].split('_')[0]
    for i in range(len(rast_year_path)):
        if i == 0:
            # read dem med
            with rasterio.open(rast_year_path[i]) as dem_src:
                dem_med = dem_src.read(1)
        if i == 1:
            # read dem q1
            with rasterio.open(rast_year_path[i]) as dem_src:
                dem_q1 = dem_src.read(1)
        if i == 2:
            # read dem q3
            with rasterio.open(rast_year_path[i]) as dem_src:
                dem_q3 = dem_src.read(1)
        if i == 3:
            # read ndvi med
            with rasterio.open(rast_year_path[i]) as ndvi_src:
                ndvi_med = ndvi_src.read(1)
        if i == 4:
            # read ndvi q1 
            with rasterio.open(rast_year_path[i]) as ndvi_src:
                ndvi_q1 = ndvi_src.read(1)
        if i == 5:
            # read ndvi q3
            with rasterio.open(rast_year_path[i]) as ndvi_src:
                ndvi_q3 = ndvi_src.read(1)
        if i == 6:
            # read ortho med
            with rasterio.open(rast_year_path[i]) as ortho_src:
                ortho_med_1 = ortho_src.read(1)
                ortho_med_2 = ortho_src.read(2)
                ortho_med_3 = ortho_src.read(3)
                ortho_med_4 = ortho_src.read(4)
                ortho_med_5 = ortho_src.read(5)
        if i == 7:
            # read ortho q1
            with rasterio.open(rast_year_path[i]) as ortho_src:
                ortho_q1_1 = ortho_src.read(1)
                ortho_q1_2 = ortho_src.read(2)
                ortho_q1_3 = ortho_src.read(3)
                ortho_q1_4 = ortho_src.read(4)
                ortho_q1_5 = ortho_src.read(5)
        if i == 8:
            # read ortho q3
            with rasterio.open(rast_year_path[i]) as ortho_src:
                ortho_q3_1 = ortho_src.read(1)
                ortho_q3_2 = ortho_src.read(2)
                ortho_q3_3 = ortho_src.read(3)
                ortho_q3_4 = ortho_src.read(4)
                ortho_q3_5 = ortho_src.read(5)
                
            # metadata for stacked raster ouput
            meta = dem_src.meta
            meta.update(nodata = None, count = 21)
            
            # write stacked raster output
            with rasterio.open(f'01_output/02_stack_rast/{year}_stack.tif',mode='w',**meta) as dst:
                dst.write_band(1, dem_med)
                dst.write_band(2, dem_q1)
                dst.write_band(3, dem_q3)
                dst.write_band(4, ndvi_med)
                dst.write_band(5, ndvi_q1)
                dst.write_band(6, ndvi_q3)
                dst.write_band(7, ortho_med_1)
                dst.write_band(8, ortho_med_2)
                dst.write_band(9, ortho_med_3)
                dst.write_band(10, ortho_med_4)
                dst.write_band(11, ortho_med_5)
                dst.write_band(12, ortho_q1_1)
                dst.write_band(13, ortho_q1_2)
                dst.write_band(14, ortho_q1_3)
                dst.write_band(15, ortho_q1_4)
                dst.write_band(16, ortho_q1_5)
                dst.write_band(17, ortho_q3_1)
                dst.write_band(18, ortho_q3_2)
                dst.write_band(19, ortho_q3_3)
                dst.write_band(20, ortho_q3_4)
                dst.write_band(21, ortho_q3_5)
                
    


