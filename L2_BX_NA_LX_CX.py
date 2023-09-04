# Make sure you have ArcGIS Pro installed (the code worked on v3.0.3)
# Open Python Command Prompt
# Navigate to the following directory
# cd C:\Users\PHYS3009\Desktop\Plastics_NetCDF\L2
# Run the code
# python L2_BX_NA_LX_CX.py



import arcpy
import os

# Directories and workspace setup
vector_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Vectors"
raster_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\L2\L2_BX_NA"
output_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\L2\L2_BX_NA_LX_CX"
arcpy.env.workspace = raster_dir
arcpy.env.overwriteOutput = True

# List of relevant shapefiles
shapefiles = [shp for shp in os.listdir(vector_dir) if shp.startswith("Lake") and (shp.endswith("_CAN.shp") or shp.endswith("_USA.shp"))]

# For each shapefile, clip all rasters in raster_dir
for shp in shapefiles:
    # Derive lake and country from shapefile name
    lake = shp.split("Lake")[1].split("_")[0]
    country = shp.split("_")[1]
    if country == "USA":
        country_code = "CUSA"
    else:
        country_code = "CCAN"
    
    # Define the full path to the shapefile
    shp_path = os.path.join(vector_dir, shp)
    
    # Clip each raster using the shapefile
    for raster in arcpy.ListRasters():
        # Define the output raster name
        output_name = f"L2_{raster.split('_')[1]}_NA_L{lake}_{country_code}.tif"
        output_path = os.path.join(output_dir, output_name)
        
        # Clip the raster
        arcpy.Clip_management(raster, "#", output_path, shp_path, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
