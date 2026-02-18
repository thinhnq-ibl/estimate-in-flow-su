import geopandas as gpd

gdf = gpd.read_file("amount_in_to_cell.geojson")


gdf["cell_in"] = gdf["intersect_area_m2"] * gdf["in_density"]

# Save the result
gdf.to_file("amount_in_to_cell.geojson", driver='GeoJSON')

print(gdf[['cell_id', 'cell_in']].head())