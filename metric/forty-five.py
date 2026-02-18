import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geopandas as gpd

# 1. Prepare your data (Example: Observed vs GEOGloWS Simulated)
# observed = [values...]
# simulated = [values...]

# Dummy data for demonstration
# np.random.seed(42)
# observed = np.random.uniform(10, 100, 50)
# simulated = observed + np.random.normal(0, 10, 50) # Simulated with some error

observed = []

simulated = []

gpd_real = gpd.read_file("../calculate_out_cell/in_flow_cells_normalized_real.geojson")
gpd_simulate = gpd.read_file("../calculate_out_cell/in_flow_cells_normalized.geojson")

for index, row in gpd_simulate.iterrows():
    cell_id = row["cell_id"]
    real = gpd_real[gpd_real["cell_id"] == cell_id]
    if len(real) > 0:
        simulated.append(row["norm_in_amount"])
        observed.append(real["norm_total_in"].iloc[0])

# 2. Create the plot
plt.figure(figsize=(8, 8))
plt.scatter(observed, simulated, color='blue', alpha=0.6, label='Data Points')

# 3. Add the 45-degree (1:1) reference line
# We find the min and max across both datasets to ensure the line covers the full range
limit_min = min(min(observed), min(simulated))
limit_max = max(max(observed), max(simulated))
plt.plot([limit_min, limit_max], [limit_min, limit_max], color='red', linestyle='--', label='1:1 Line (Perfect Match)')

# 4. Format the plot
plt.xlabel('Observed Streamflow 2 ($m^3/s$)')
plt.ylabel('GEOGloWS Simulated Streamflow 2 ($m^3/s$)')
plt.title('Validation: Observed vs Simulated (GEOGloWS) 2')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

# Crucial: Ensure the axes are equal so the 45-degree line is actually 45 degrees
plt.axis('equal')
plt.xlim(limit_min, limit_max)
plt.ylim(limit_min, limit_max)

plt.show()