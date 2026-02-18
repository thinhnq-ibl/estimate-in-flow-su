# import geopandas as gpd

# # 1. Read the shapefile
# # Provide the path to the .shp file
# path_to_shapefile = 'map/data_seoul_subzone.shp'
# gdf = gpd.read_file(path_to_shapefile)

# # 2. Check the data
# print("--- Data Info ---")
# print(gdf.info())
# print("\n--- First 5 Rows ---")
# print(gdf.head())

# # 3. Check the Coordinate Reference System (CRS)
# # Very important for mapping coordinates like 127.02, 37.64
# print(f"\nCoordinate System: {gdf.crs}")

# # 4. Simple Visualization
# # This will open a plot showing the geographic shapes
# gdf.plot()

import geopandas as gpd
import matplotlib.pyplot as plt

# Load your shapefile
gdf = gpd.read_file('map/data_seoul_subzone.shp')

print(gdf)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the shapefile
gdf.plot(ax=ax, color='lightgrey', edgecolor='white')

# Add titles and labels
plt.title('Subzone Geographic Distribution', fontsize=15)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.show()