# Make sure you have ArcGIS Pro installed (the code worked on v3.0.3)
# Open Python Command Prompt
# Navigate to the following directory
# cd C:\Users\PHYS3009\Desktop\Plastics_NetCDF
# Run the code
# python Raster_Bin_Sum_USCAN.py
# Also make sure the following libraries are installed: pandas and numpy, if not, use the following code in Windows Command Prompt:
# pip install pandas numpy



import arcpy
import os
import pandas as pd
import numpy as np
arcpy.env.overwriteOutput = True


# Defining directories
workspace_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Output_Rasters_Resampled"
arcpy.env.workspace = workspace_dir

output_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Layer2_Sum"
clip_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Layer2_Sum_Subbasins_USCAN"
watersheds_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Vectors"
csv_dir = r"C:\Users\PHYS3009\Desktop\Plastics_NetCDF\Layer2_Sum_Subbasins_USCAN"

watersheds = ["greatlakes_subbasins_erie_us.shp", "greatlakes_subbasins_huron_us.shp",
              "greatlakes_subbasins_ontario_us.shp", "greatlakes_subbasins_michigan_us.shp",
              "greatlakes_subbasins_superior_us.shp", "greatlakes_subbasins_erie_can.shp",
              "greatlakes_subbasins_huron_can.shp", "greatlakes_subbasins_ontario_can.shp",
              "greatlakes_subbasins_michigan_can.shp", "greatlakes_subbasins_superior_can.shp"]
bin_values = {1: (0.3**3)*1.22*(10**-3), 2: (2.5**3)*1.22*(10**-3),
              3: (7**3)*1.22*(10**-3), 4: (15**3)*1.22*(10**-3),
              5: (35**3)*1.22*(10**-3), 6: (70**3)*1.22*(10**-3)}

# Permission for creating required directories if not present
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(clip_dir):
    os.makedirs(clip_dir)

# Creating an empty dataframe for final table
df_final = pd.DataFrame(columns=["FileName", "Sum of Pixel Values (kg/m2/s)", "Microplastic Counts"])

# Writing a loop for nvars and bin in layer_2
for bin_num in range(1, 7):
    rasters_to_sum = []
    for var_num in range(1, 6):
        raster_file = f"layer2_bin{bin_num}_nvars{var_num}_Resample2.tif"
        raster_path = os.path.join(workspace_dir, raster_file)
        if os.path.isfile(raster_path):
            rasters_to_sum.append(arcpy.Raster(raster_path))

    if rasters_to_sum:  # Ensure list is not empty
        # Use arcpy's cell by cell addition for rasters
        output_raster = rasters_to_sum[0]
        for raster in rasters_to_sum[1:]:
            output_raster += raster

        output_name = f"l2_b{bin_num}_na.tif"
        output_raster.save(os.path.join(output_dir, output_name))

        # Clipping the rasters to shape files
        for watershed in watersheds:
            watershed_name = watershed.split('_')[2]
            country = watershed.split('_')[3].split('.')[0]
            clipped_raster_name = f"l2_b{bin_num}_na_s_{watershed_name}_{country}.tif"
            
            try:
                arcpy.Clip_management(os.path.join(output_dir, output_name), "#", os.path.join(clip_dir, clipped_raster_name),
                                      os.path.join(watersheds_dir, watershed), "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")

                # Calculating the sum of pixel values for each raster
                clipped_raster = arcpy.Raster(os.path.join(clip_dir, clipped_raster_name))
                data = arcpy.RasterToNumPyArray(clipped_raster, nodata_to_value=np.nan)
                sum_pixel_values = np.nansum(data)
                sum_pixel_values = f'{sum_pixel_values:.4e}'  # Converting to scientific notation

                # Creating a calculated column based on bin values
                calculated_value = float(sum_pixel_values) / bin_values[bin_num]
                calculated_value = f'{calculated_value:.4e}'  # Converting to scientific notation
            except:
                sum_pixel_values = np.nan
                calculated_value = np.nan
            
            # Attaching to the final dataframe
            df_final = df_final.append({"FileName": clipped_raster_name,
                                        "Sum of Pixel Values (kg/m2/s)": sum_pixel_values,
                                        "Microplastic Counts": calculated_value}, ignore_index=True)
print(df_final)

# Creating a second table with the sum of calculated values for each watershed, converted to days
df_final = df_final.replace('nan', np.nan)
df_final['Microplastic Counts'] = df_final['Microplastic Counts'].astype(float)  
df_final['Watershed'] = df_final['FileName'].apply(lambda x: '_'.join(x.split('_')[-2:]).split('.')[0])  # Extracting watershed name
df_sum = df_final.groupby('Watershed')['Microplastic Counts'].sum() * 60 * 60 * 24 # Unit conversion (per second → per day)

# Reporting in scientific notation
df_sum_dict = {watershed: '{:.4e}'.format(value) if not pd.isna(value) else np.nan for watershed, value in df_sum.items()}
df_sum_df = pd.DataFrame(list(df_sum_dict.items()), columns=["Watershed", "? Per Days"])
print(df_sum_df)


# Save dataframes to csv files named
df_final.to_csv(os.path.join(csv_dir, "table1_USCAN.csv"), index=False)
df_sum_df.to_csv(os.path.join(csv_dir, "table2_USCAN.csv"), index=False)
