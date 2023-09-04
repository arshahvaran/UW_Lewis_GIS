# Make sure you have ArcGIS Pro installed (the code worked on v3.0.3)
# Open Python Command Prompt
# Navigate to the following directory
# cd C:\Users\PHYS3009\Desktop\Plastics_NetCDF
# Run the code
# python Report.py



import arcpy
import os
import pandas as pd

# Define paths and initialize lists
base_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF"
output_excel = os.path.join(base_dir, "Report.xlsx")
file_names = []
sum_values = []

# Traverse directory to find relevant .tif files
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".tif") and (file.startswith("L1") or file.startswith("L2") or file.startswith("L3")):
            file_path = os.path.join(root, file)
            
            # Get the mean pixel value using ArcPy
            mean_value = float(arcpy.GetRasterProperties_management(file_path, "MEAN").getOutput(0))
            
            # Convert raster to numpy array to compute the count of valid pixels
            raster_array = arcpy.RasterToNumPyArray(file_path, nodata_to_value=float('nan'))
            valid_pixel_count = (~numpy.isnan(raster_array)).sum()
            
            # Compute the sum of pixel values
            sum_pixel = mean_value * valid_pixel_count
            
            # Append results to lists
            file_names.append(file.replace(".tif", ""))
            sum_values.append(sum_pixel)

# Create a DataFrame and save to Excel
df = pd.DataFrame({
    "File Name": file_names,
    "Sum of Pixel Values": sum_values
})

df.to_excel(output_excel, index=False)


