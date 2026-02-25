import numpy as np
import pandas as pd

# 1. Prepare your data (Example: Observed vs GEOGloWS Simulated)
# observed = [values...]
# simulated = [values...]

# Dummy data for demonstration
# np.random.seed(42)
# observed = np.random.uniform(10, 100, 50)
# simulated = observed + np.random.normal(0, 10, 50) # Simulated with some error



# Read as CSV (not GeoDataFrame) and ensure numeric columns
gpd_real = pd.read_csv("../calculate_in_cell/all_flow_cell.csv")
gpd_simulate = pd.read_csv("../calculate_out_cell/all_flow_cell.csv")



# Ensure in_amount is numeric (in case of string/object type)
gpd_real['in_amount'] = pd.to_numeric(gpd_real['in_amount'], errors='coerce').fillna(0)
gpd_simulate['in_amount'] = pd.to_numeric(gpd_simulate['in_amount'], errors='coerce').fillna(0)

def fast_cpc(df_obs, df_pred):
    """
    High-performance CPC calculation for large datasets.
    """
    # Ensure in_amount columns are numeric
    df_obs = df_obs.copy()
    df_pred = df_pred.copy()
    df_obs['in_amount'] = pd.to_numeric(df_obs['in_amount'], errors='coerce').fillna(0)
    df_pred['in_amount'] = pd.to_numeric(df_pred['in_amount'], errors='coerce').fillna(0)

    # 1. Use an inner merge to find the intersection of flows
    merged = pd.merge(
        df_obs[['origin_cell', 'destination_cell', 'in_amount']], 
        df_pred[['origin_cell', 'destination_cell', 'in_amount']], 
        on=['origin_cell', 'destination_cell'], 
        suffixes=('_obs', '_pred')
    )
    # 2. Convert columns to NumPy arrays (Zero-copy view if possible)
    obs_flows = merged['in_amount_obs'].values.astype(float)
    pred_flows = merged['in_amount_pred'].values.astype(float)
    # 3. Vectorized minimum and sums
    intersection_sum = np.minimum(obs_flows, pred_flows).sum()
    # Calculate totals from the original dataframes to account for flows that might exist in one but not the other
    total_obs = merged['in_amount_obs'].sum()
    total_pred = merged['in_amount_pred'].sum()
    # 4. Final CPC Ratio
    cpc = (2.0 * intersection_sum) / (total_obs + total_pred)
    return cpc

# Example Usage:
cpc_score = fast_cpc(gpd_real, gpd_simulate)
print(f"CPC Score: {cpc_score:.4f}")
