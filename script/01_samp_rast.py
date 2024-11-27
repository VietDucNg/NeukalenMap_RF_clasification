# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:56:12 2024

@author: Viet Nguyen (https://vietducng.github.io/)
University of Greifswald (https://geo.uni-greifswald.de/en/eo)
"""

import os
import glob
from osgeo import gdal
from multiprocessing import Pool
import time

# set wd
os.getcwd()
os.chdir(os.getcwd().replace('\\script',''))
os.getcwd()

# Tell GDAL to throw Python exceptions, and register all drivers
gdal.UseExceptions()
gdal.AllRegister()

#### data paths
# raw raster paths (raw dem + orthomosaic)
raw_rast_paths = glob.glob('00_data/*.tif')
print('\n Raw raster paths:')
print(raw_rast_paths)

# prep raster directory (clip and aggregate)
prep_rast_dir = '01_output/01_prep_rast/'

# list of quantiles for resampling
quantiles = ['med','q1','q3']

### function to clip and resampling raster
def clip_func(path):
  name = path.split('\\')[1].split('.')[0]
  print(f'\n clipping {name} ...\n')
  for quantile in quantiles:
      with gdal.Open(path) as source:
          gdal.Warp(destNameOrDestDS = f'{prep_rast_dir}{name}_clip_50cm_{quantile}.tif',
                    srcDSOrSrcDSTab = source,
                    options=f'-t_srs EPSG:5650 -of GTiff -ot Float32\
                        -cutline 00_data/area_studysite.shp \
                            -cl area_studysite -crop_to_cutline \
                                -tr 0.5 0.5 -r {quantile}\
                                    -multi -co NUM_THREADS=ALL_CPUS -wo NUM_THREADS=ALL_CPUS \
                                        -co TILED=YES -co BIGTIFF=YES') 
                                    # -co COMPRESS=DEFLATE 
                                    
  print(f'\n Done {name}_clip !\n')
  source = None
  return None

if __name__ == "__main__":
  # Use multiprocessing Pool to process rasters in parallel
  start_time = time.time()
  with Pool(processes = os.cpu_count()) as pool:
    pool.map(clip_func, raw_rast_paths)
    pool.close()
  end_time = time.time()
  print(f"Elapsed time: {(end_time - start_time)/60} minutes")




########### gdal approach with keywords ##########
# no compress option
# for i in range(len(raster_paths)):
#     name = raster_paths[i].split('\\')[1].split('.')[0]
#     print(f'\n clipping {name} ...\n')
#     gdal.Warp(destNameOrDestDS = f'01_output/01_prep_data/{name}_clip.tif', 
#               srcDSOrSrcDSTab = raster_paths[i],
#               format = 'GTiff', dstSRS = 'EPSG:5650', multithread = True,
#               cutlineDSName = '00_data/area_studysite.shp', 
#               cutlineLayer = 'area_studysite', cropToCutline = True)
#     print('\n Done!\n')


########### rasterio approach ###########
# #### clip rasters to AOI
# ### read AOI vector
# aoi_vect = gpd.read_file('00_data/area_studysite.shp')
# aoi_vect
# aoi_vect.crs
#
# for i in range(len(raster_paths)):
#     # read raster
#     with rasterio.open(raster_paths[i]) as src:
#         clipped_raster, clipped_transform = mask.mask(src, aoi_vect.geometry, crop=True)
#         meta = src.meta.copy()  # Get metadata

#     # Update metadata with new dimensions and transform
#     meta.update({
#         "driver":"Gtiff",
#         'compress': 'deflate',  # Set compression to Deflate
#         "height": clipped_raster.shape[1],
#         "width": clipped_raster.shape[2],
#         "transform": clipped_transform
#     })

#     # Write the clipped raster to a new file
#     with rasterio.open(clip_rast_paths[i], "w", **meta) as dst:
#         dst.write(clipped_raster)





