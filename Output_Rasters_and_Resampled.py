# Make sure you have ArcGIS Pro installed (the code worked on v3.0.3)
# Open Python Command Prompt
# Navigate to the following directory
# cd C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Raw_Data_Preparation
# Run the code
# python Output_Rasters_and_Resampled.py



import arcpy
import os

# Set the workspace
workspace = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Raw_Data_Preparation"
arcpy.env.workspace = workspace

# Set overwrite option
arcpy.env.overwriteOutput = True

# Input NetCDF file
input_netcdf_path = os.path.join(workspace, "Plastics_LongitudeFixed.nc")

# Define the output directories
output_rasters_dir = os.path.join(workspace, "Output_Rasters")
output_rasters_resampled_dir = os.path.join(workspace, "Output_Rasters_Resampled")

# Check if output directories exist, if not, create them
for dir_path in [output_rasters_dir, output_rasters_resampled_dir]:
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

# Define the layers, bins, and nvars
layers = ['conc', 'dep', 'source']
bins = ['1', '2', '3', '4', '5', '6']
nvars = ['1', '2', '3', '4', '5']

# Loop through each layer, bin, and nvars
for i, layer in enumerate(layers, start=1):
    for j, bin in enumerate(bins, start=1):
        for k, nvar in enumerate(nvars, start=1):
            # Output raster name
            output_raster = f'layer{i}_bin{j}_nvars{k}'
            # Create a NetCDF raster layer
            dimension_values = f"bin {bin};nvars {nvar}"
            arcpy.md.MakeNetCDFRasterLayer(input_netcdf_path, layer, "lon", "lat", output_raster, "", dimension_values, "By value", "Center")
            
            # Define the tiff file paths
            tiff_file = os.path.join(output_rasters_dir, f'{output_raster}.tif')
            resampled_file = os.path.join(output_rasters_resampled_dir, f'{output_raster}_Resample2.tif')

            # Save the raster layer as a TIFF file
            arcpy.management.CopyRaster(output_raster, tiff_file, "", "", "", "NONE", "NONE", "")

            # Define the projection
            arcpy.management.DefineProjection(tiff_file, 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]')

            # Resample the raster
            arcpy.management.Resample(tiff_file, resampled_file, "0.1 0.1", "BILINEAR")
