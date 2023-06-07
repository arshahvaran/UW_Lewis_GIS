# Make sure you have ArcGIS Pro installed (the code worked on v3.0.3)
# Open Python Command Prompt
# Navigate to the following directory
# cd C:\Users\PHYS3009\Desktop\Plastics_NetCDF
# Run the code
# python Preparaing_NC_for_Spatial_Analysis.py



import arcpy
import os

# Adding the directory of the input rasters
dir_path = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Output_Rasters_Resampled"
# Setting workspace
arcpy.env.workspace = dir_path

# Defining output directory
output_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Layer2_Sum"
# Defining output raster name
output_name = "layer2_sum.tif"

# Create a list to store the raster objects to sum
rasters_to_sum = []

# Loop through all tif files in the specified directory
for file in os.listdir(dir_path):
    if file.endswith(".tif") and file.startswith("layer2"):
        rasters_to_sum.append(arcpy.Raster(os.path.join(dir_path, file)))

# Calculate the sum of all the rasters
output_raster = rasters_to_sum[0]
for raster in rasters_to_sum[1:]:
    output_raster += raster

# Check if the output directory exists, if not, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the output raster
output_raster.save(os.path.join(output_dir, output_name))
