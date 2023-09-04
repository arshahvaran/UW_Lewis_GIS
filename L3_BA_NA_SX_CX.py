# Make sure you have ArcGIS Pro installed (the code worked on v3.0.3)
# Open Python Command Prompt
# Navigate to the following directory
# cd C:\Users\PHYS3009\Desktop\Plastics_NetCDF\L3
# Run the code
# python L3_BA_NA_SX_CX.py



import arcpy
import os

# Directories and workspace setup
vector_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Vectors"
raster_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\L3\L3_BA_NA"
output_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\L3\L3_BA_NA_SX_Cx"
arcpy.env.workspace = raster_dir
arcpy.env.overwriteOutput = True

# List of relevant shapefiles
shapefiles = [shp for shp in os.listdir(vector_dir) if shp.startswith("greatlakes_subbasins_") and (shp.endswith("_can.shp") or shp.endswith("_us.shp"))]

# For each shapefile, clip all rasters in raster_dir
for shp in shapefiles:
    # Skip the specified shapefile
    if shp == "greatlakes_subbasins_michigan_can.shp":
        continue

    # Derive basin and country from shapefile name
    basin = shp.split("_")[2]
    country = shp.split("_")[3]
    
    # Define the full path to the shapefile
    shp_path = os.path.join(vector_dir, shp)
    
    # Clip each raster using the shapefile
    for raster in arcpy.ListRasters():
        # Define the output raster name
        output_name = f"L3_BA_NA_S{basin}_C{country}.tif"
        output_path = os.path.join(output_dir, output_name)
        
        # Clip the raster
        arcpy.Clip_management(raster, "#", output_path, shp_path, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

