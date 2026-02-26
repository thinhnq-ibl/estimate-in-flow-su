import geopandas as gpd
import pandas as pd

# 1. Load and Project
gdf = gpd.read_file('final_summed_out_cells.geojson').to_crs(epsg=3857)

# Calculate Centroids and Total Area up front
gdf['centroid'] = gdf.geometry.centroid
gdf['total_area_sqm'] = gdf.geometry.area

# Create a lookup for both Area and Centroid Geometry
cell_data_lookup = gdf[['cell_id', 'total_area_sqm', 'centroid']].set_index('cell_id')

# 2. Define Ring Geometries (Donuts)
b1 = gdf.buffer(1000)
b10 = gdf.buffer(10000)
b20 = gdf.buffer(20000)

rings = gdf[['cell_id']].copy()
rings['ring_0_1'] = b1
rings['ring_1_10'] = b10.difference(b1)
rings['ring_10_20'] = b20.difference(b10)

# 3. Calculate Intersections
results = []
for ring_col in ['ring_0_1', 'ring_1_10', 'ring_10_20']:
    ring_gdf = gpd.GeoDataFrame(rings[['cell_id']], geometry=rings[ring_col], crs=gdf.crs)
    
    # Intersect rings (source) with original cells (neighbor)
    intersections = gpd.overlay(ring_gdf, gdf[['cell_id', 'geometry']], how='intersection')
    intersections = intersections.rename(columns={'cell_id_1': 'source_cell', 'cell_id_2': 'neighbor_cell'})
    
    # Remove self-matches
    intersections = intersections[intersections['source_cell'] != intersections['neighbor_cell']]
    
    intersections['overlap_area_sqm'] = intersections.geometry.area
    intersections['ring_type'] = ring_col
    results.append(intersections[['source_cell', 'neighbor_cell', 'ring_type', 'overlap_area_sqm']])

# 4. Merge and Calculate Metrics
final_df = pd.concat(results)

# Map Neighbor Area and Source/Neighbor Centroids
final_df['neighbor_total_area'] = final_df['neighbor_cell'].map(cell_data_lookup['total_area_sqm'])
final_df['source_centroid'] = final_df['source_cell'].map(cell_data_lookup['centroid'])
final_df['neighbor_centroid'] = final_df['neighbor_cell'].map(cell_data_lookup['centroid'])

# A. Calculate Overlap Percentage
final_df['overlap_pct'] = (final_df['overlap_area_sqm'] / final_df['neighbor_total_area']) * 100

# B. Calculate Centroid-to-Centroid Distance (Vectorized)
# We use the .distance() method on the Series of points
final_df['centroid_dist_m'] = final_df.apply(
    lambda row: row['source_centroid'].distance(row['neighbor_centroid']), axis=1
)

# 5. Final Cleanup
final_df = final_df.drop(columns=['source_centroid', 'neighbor_centroid'])
cols_to_show = ['source_cell', 'neighbor_cell', 'ring_type', 'centroid_dist_m', 'overlap_area_sqm', 'overlap_pct']
output = final_df[cols_to_show].round(2)

output.to_csv('cells_split_by_rings.csv', index=False)
print(output.head())