import geopandas as gpd

gdf = gpd.read_file("amount_out_from_cell.geojson")


gdf["total_out"] = gdf["intersect_area_m2"] * gdf["final_out_value"]

# Save the result
gdf.to_file("amount_out_from_cell.geojson", driver='GeoJSON')

print(gdf[['cell_id', 'final_out_value']].head())