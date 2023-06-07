import xarray as xr

# Open the NetCDF file
ds = xr.open_dataset('plastics.nc')

# Subtract 180 from all longitudes
ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180

# Reorder the dataset so that the longitude coordinates are increasing
ds = ds.sortby('lon')

# Save the modified dataset to a new NetCDF file
ds.to_netcdf('modified_plastics.nc')
