import geopandas as gpd

gdf = gpd.read_file("all_bounded_in_cells.geojson")


gdf["cell_in"] = gdf["intersect_area_m2"] * gdf["in_density"]

# Save the result
gdf.to_file("all_bounded_in_cells.geojson", driver='GeoJSON')

print(gdf[['cell_id', 'cell_in']].head())