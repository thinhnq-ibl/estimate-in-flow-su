import geopandas as gpd
import pandas as pd
import numpy as np

# 1. Load and Project to an EQUAL AREA CRS (Crucial for area accuracy)
# EPSG:6933 is a global equal-area projection

# Read CSV with pandas, aggregate area
# df = pd.read_csv('cells_split_by_rings.csv')
# df2 = df.groupby('cell_id', as_index=False)['area_sqkm'].sum()
# df2.to_csv('cells_split_by_rings2.csv', index=False)

df = gpd.read_file('all_bounded_out_cells.geojson')

df2 = df.groupby('cell_id', as_index=False)['intersect_area_m2'].sum()
df2.to_csv('cells_split_by_rings2.csv', index=False)