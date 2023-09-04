# Make sure you have ArcGIS Pro installed (the code worked on v3.0.3)
# Open Python Command Prompt
# Navigate to the following directory
# cd C:\Users\PHYS3009\Desktop\Plastics_NetCDF\L2
# Run the code
# python L2_BX_NA.py



import arcpy
import os

# Adding the directory of the input rasters
dir_path = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Raw_Data_Preparation\Output_Rasters_Resampled"
# Setting workspace
arcpy.env.workspace = dir_path
arcpy.env.overwriteOutput = True

# Defining output directory
output_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\L2\L2_BX_NA"

# Loop through each bin (from 1 to 6) for layer 2
for bin_num in range(1, 7):
    rasters_to_sum = []
    
    # Loop through all tif files in the specified directory for the current bin
    for file in os.listdir(dir_path):
        if file.endswith(".tif") and file.startswith(f"layer2_bin{bin_num}_nvars"):
            rasters_to_sum.append(arcpy.Raster(os.path.join(dir_path, file)))
    
    # Calculate the sum of all the rasters for the current bin
    output_raster = rasters_to_sum[0]
    for raster in rasters_to_sum[1:]:
        output_raster += raster
    
    # Define the output raster name for the current bin
    output_name = f"L2_B{bin_num}_NA.tif"
    
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the summed raster for the current bin
    output_raster.save(os.path.join(output_dir, output_name))
