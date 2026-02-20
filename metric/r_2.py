import geopandas as gpd
import numpy as np

observed = []
simulated = []

gpd_real = gpd.read_file("../calculate_in_cell/in_flow_cells_normalized_real.geojson")
gpd_simulate = gpd.read_file("../calculate_out_cell/in_flow_cells_normalized.geojson")

for index, row in gpd_simulate.iterrows():
    cell_id = row["cell_id"]
    real = gpd_real[gpd_real["cell_id"] == cell_id]
    if len(real) > 0:
        simulated.append(row["total_in"])
        observed.append(real["cell_in"].iloc[0])

# Convert lists to numpy arrays
observed = np.array(observed)
simulated = np.array(simulated)

# 1. Residual Sum of Squares (Error)
ss_res = ((observed - simulated)**2).sum()

# 2. Total Sum of Squares (Variance in actual data)
ss_tot = ((observed - simulated.mean())**2).sum()

# 3. Final R-squared
r2 = 1 - (ss_res / ss_tot)

print(f"R-squared: {r2}")