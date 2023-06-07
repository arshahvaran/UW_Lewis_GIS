# Make sure you have ArcGIS Pro installed (the code worked on v3.0.3)
# Open Python Command Prompt
# Navigate to the following directory
# cd C:\Users\PHYS3009\Desktop\Plastics_NetCDF
# Run the code
# python Clipping_Subbasins.py


import arcpy
import os
import numpy as np

# Loading the directories
shape_files_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Vectors"
raster_to_clip = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Layer2_Sum\layer2_sum.tif"
output_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Layer2_Sum_Subbasins"

# Check if the output directory exists, if not, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Shapefile names and corresponding output names
shapefile_names = ['greatlakes_subbasins_erie', 'greatlakes_subbasins_huron', 
                   'greatlakes_subbasins_michigan', 'greatlakes_subbasins_ontario', 
                   'greatlakes_subbasins_superior']
output_names = ['layer2_sum_subbasins_erie', 'layer2_sum_subbasins_huron', 
                'layer2_sum_subbasins_michigan', 'layer2_sum_subbasins_ontario', 
                'layer2_sum_subbasins_superior']

# Loop through each shapefile and perform the clipping
for shapefile_name, output_name in zip(shapefile_names, output_names):
    # Full path to the shapefile
    shapefile_path = os.path.join(shape_files_dir, shapefile_name + '.shp')
    
    # Full path for the output
    output_path = os.path.join(output_dir, output_name + '.tif')
    
    # Clip the raster
    arcpy.management.Clip(raster_to_clip, None, output_path, shapefile_path, '', "ClippingGeometry", "MAINTAIN_EXTENT")

# Calculating sum of pixel values for each clipped raster
print("Clipped Raster Name\t\tSum of Pixel Values (kg/m2/s)")
for output_name in output_names:
    output_path = os.path.join(output_dir, output_name + '.tif')
    
    # Convert raster to numpy array
    raster_array = arcpy.RasterToNumPyArray(output_path)
    
    # Exclude NoData values
    raster_array = raster_array[raster_array != arcpy.Raster(output_path).noDataValue]
    
    # Calculate the sum of pixel values
    sum_pixel_values = np.nansum(raster_array)  # use np.nansum to handle possible NaNs and infinites
    
    print(f"{output_name}\t\t{sum_pixel_values:.4E}")  # use :.4E to print sum in scientific notation


