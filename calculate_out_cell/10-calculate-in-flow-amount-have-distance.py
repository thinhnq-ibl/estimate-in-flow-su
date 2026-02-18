import geopandas as gpd

geojson_file = "categorized_cell_pairs.geojson"
pair_cell_gdf = gpd.read_file(geojson_file)

# 1. Load your GeoJSON
gdf = gpd.read_file('seoul_prob_pois.geojson')

gdf['in_amount'] = 0

# Extract the first cell_id as a scalar value (not a Series)
for index1, row1 in gdf.iterrows():
    first_cell_id = row1["cell_id"]  # row1["cell_id"] is already a scalar, no need for .iloc[0]
    # print(f"First cell ID: {first_cell_id}")

    # Now filter using the scalar value
    all_pairs = pair_cell_gdf[pair_cell_gdf["cell_id"] == first_cell_id].copy()
    # print(f"Found {len(all_pairs)} pairs")

    sum_in = 0
    for index, row in all_pairs.iterrows():
        sum_in += float(row["in_amount"])
    
    gdf.at[index1, "total_in"] = sum_in
   
gdf.to_file("in_flow_cells_distance.geojson", driver='GeoJSON')