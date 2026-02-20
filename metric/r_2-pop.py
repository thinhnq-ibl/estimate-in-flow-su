import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd

gpd_real = gpd.read_file("../calculate_in_cell/in_flow_cells_normalized_real.geojson")
gpd_simulate = gpd.read_file("../calculate_in_by_pop/in_flow_cells_distance.geojson")

# 1. Residual Sum of Squares (Error)
ss_res = ((gpd_real['total_in'] - gpd_simulate['total_in'])**2).sum()

# 2. Total Sum of Squares (Variance in actual data)
ss_tot = ((gpd_real['total_in'] - gpd_simulate['total_in'].mean())**2).sum()

# 3. Final R-squared
r2 = 1 - (ss_res / ss_tot)

print(f"R-squared: {r2}")