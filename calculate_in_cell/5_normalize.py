import geopandas as gpd
import pandas as pd

# 1. Load your GeoJSON data
# Replace 'in_flow_cells_v2_distance.json' with your actual file path
gdf = gpd.read_file('in_flow_cells_normalized_real.geojson')

# 2. Calculate the total sum of all inflows
total_in_flow = gdf['cell_in'].sum()

# 3. Normalize each in_amount by the total sum
# This gives you the proportion of total flow for each cell
gdf['norm_total_in'] = gdf['cell_in'] / total_in_flow

# 4. Optional: Verify the sum of normalized values is 1.0
print(f"Total In-Amount: {total_in_flow}")
print(f"Sum of Normalized: {gdf['norm_total_in'].sum()}")

gdf.sort_values("cell_id")
# 5. Save the updated data to a new file
gdf.to_file('in_flow_cells_normalized_real.geojson', driver='GeoJSON')

# Display the first few rows to verify
print(gdf[['cell_id', 'cell_in', 'norm_total_in']].head())