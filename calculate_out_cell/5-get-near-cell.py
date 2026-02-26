import geopandas as gpd

# 1. Load and Project
gdf = gpd.read_file('final_summed_out_cells.geojson').reset_index()
gdf = gdf.to_crs(epsg=4326) 

# 2. Define thresholds
threshold_near = 0.00833   # 1km
threshold_far = 10 * 0.00833   # 10km
threshold_over = 20 * 0.00833   # 20km

# 3. Create a buffer for the maximum search area (10km)
# We keep 'cell_id' in this copy so it's available after the join
gdf_buffered = gdf[['cell_id', 'geometry']].copy()
gdf_buffered['geometry'] = gdf_buffered.buffer(threshold_over)

# 4. Spatial Join
# We join the original points (left) with the 10km buffers (right)
nearby = gpd.sjoin(
    gdf[['cell_id', 'geometry']], 
    gdf_buffered, 
    predicate='intersects', 
    how='inner'
).rename(columns={'cell_id_left': 'cell_id', 'cell_id_right': 'neighbor_id'})

# 5. Clean up: Remove self-matches and duplicates
# Using cell_id comparison to ensure we don't match a cell to itself
# nearby = nearby[nearby['cell_id'] != nearby['neighbor_id']]

# To avoid A-B and B-A duplicates, we sort and drop
# This is cleaner than index comparison when dealing with specific IDs
nearby['pair_key'] = nearby.apply(lambda x: "-".join(sorted([str(x['cell_id']), str(x['neighbor_id'])])), axis=1)
nearby = nearby.drop_duplicates(subset=['pair_key']).drop(columns=['pair_key'])

# 6. Calculate exact distance to categorize
def calculate_distance(row):
    # Lookup the original geometries using the cell_ids
    geom_a = gdf.loc[gdf['cell_id'] == row['cell_id'], 'geometry'].values[0]
    geom_b = gdf.loc[gdf['cell_id'] == row['neighbor_id'], 'geometry'].values[0]
    return geom_a.distance(geom_b)

nearby['distance_m'] = nearby.apply(calculate_distance, axis=1)

# 7. Categorize
nearby['category'] = '10km-20km'
nearby.loc[nearby['distance_m'] <= threshold_far, 'category'] = '1km-10km'
nearby.loc[nearby['distance_m'] <= threshold_near, 'category'] = 'under_1km'

# 8. Export
output_gdf = nearby.to_crs(epsg=4326)
output_gdf.to_file("categorized_cell_pairs.geojson", driver='GeoJSON')

print(output_gdf[['cell_id', 'neighbor_id', 'distance_m', 'category']].head())