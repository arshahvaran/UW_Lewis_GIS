# Before running the code, follow the next steps:

# in Anaconda Prompt run this codes one by one in order
# conda create -n plastics_env python=3.9
# conda activate plastics_env
# conda install -c conda-forge xarray netcdf4 rasterio
# make sure these three libraries are in the list: xarray netcdf4 rasterio
# conda list



import xarray as xr

# Open the NetCDF file
ds = xr.open_dataset('plastics.nc')

# Subtract 180 from all longitudes
ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180

# Reorder the dataset so that the longitude coordinates are increasing
ds = ds.sortby('lon')

# Save the modified dataset to a new NetCDF file
ds.to_netcdf('modified_plastics.nc')

# For running the code, follow the next steps:
# navigate to the directory of the original nc file in Anaconda Prompt
# The following is the directory at which the plastics.nc is stored ↓
# cd C:\Users\PHYS3009\Desktop\Plastics_NetCDF
# run the python code for modifying the longitude of the original nc file (input lon: [0 to 360] output lon: [-180 to 180])
# python Modifying_Lon.py
