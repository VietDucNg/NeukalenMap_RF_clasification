# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 14:51:01 2024

@author: Viet Nguyen
"""

import os
import glob
import rasterio
import numpy
import matplotlib.pyplot as plt
from matplotlib import colors

# check wd
os.getcwd()
os.chdir(os.getcwd().replace('\\script', ''))
os.getcwd()

# get ortho paths
prep_ortho_paths = glob.glob('01_output/01_prep_rast/*ortho*')
prep_ortho_paths

# preprocessd raster directory (clip and aggregate in 1.1)
prep_rast_dir = '01_output/01_prep_rast/'

for path in prep_ortho_paths:
    # get base name
    year = path.split('\\')[1].split('_')[0]
    quantile = path.split('_')[7].split('.')[0]
    
    # load red and NIR band
    with rasterio.open(path) as src:
        red_band = src.read(3)
        nir_band = src.read(5)
        
    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')
        
    # calculte NDVI
    ndvi = (nir_band.astype(float) - red_band.astype(float))/(nir_band+red_band)
    
    # Set metadata spatial characteristics of the output raster to mirror the input
    kwargs = src.meta
    kwargs.update(dtype=rasterio.float32, count = 1)
    kwargs
    
    # write ndvi raster
    with rasterio.open(f'{prep_rast_dir}/{year}_ndvi_clip_50cm_{quantile}.tif', 'w', **kwargs) as dst:
        dst.write_band(1, ndvi.astype(rasterio.float32))
        
    
# check ndvi
print(numpy.nanmin(ndvi)) 
print(numpy.nanmax(ndvi))


#### plot NDVI
# Set min/max values from NDVI range for image
min=numpy.nanmin(ndvi)
max=numpy.nanmax(ndvi)

# color scheme
class MidpointNormalize(colors.Normalize):
   
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
       
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return numpy.ma.masked_array(numpy.interp(value, x, y), numpy.isnan(value))
    
# Set our custom midpoint for most effective NDVI analysis
mid=0.1

# Setting color scheme ref:https://matplotlib.org/users/colormaps.html as a reference
colormap = plt.cm.RdYlGn 
norm = MidpointNormalize(vmin=min, vmax=max, midpoint=mid)
fig = plt.figure(figsize=(20,10))


ax = fig.add_subplot(111)

# Use 'imshow' to specify the input data, colormap, min, max, and norm for the colorbar
cbar_plot = ax.imshow(ndvi, cmap=colormap, norm=norm)

# Turn off the display of axis labels 
ax.axis('off')

# Set a title 
ax.set_title('Normalized Difference Vegetation Index', fontsize=17, fontweight='bold')

# Configure the colorbar
cbar = fig.colorbar(cbar_plot, orientation='horizontal', shrink=0.65)

# Call 'savefig' to save this plot to an image file
# fig.savefig("ndvi-image.png", dpi=200, bbox_inches='tight', pad_inches=0.7)

# let's visualize
plt.show()
    
    
    
    
    
    
    