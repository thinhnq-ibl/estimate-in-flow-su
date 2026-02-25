import geopandas as gpd
import pandas as pd

# Read the shapes (subzones) and the grid of cells once
subzones = gpd.read_file('./all_bounded_in_cells.geojson')

# keep only relevant columns but preserve the geometry column so the result stays a
# GeoDataFrame (needed for GeoPandas methods like `to_file`).
cols = ["cell_id", "global_row", "global_col", "SUBZONE_C", 
        "intersect_area_m2", "group_area"]
# ensure geometry is included
cols_with_geom = cols + [subzones.geometry.name]
subzones = subzones[cols_with_geom]

subzones.to_file("map_zone_cell.geojson", driver="GeoJSON")
