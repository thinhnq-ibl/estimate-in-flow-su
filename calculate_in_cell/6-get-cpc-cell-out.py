import geopandas as gpd
import pandas as pd

# Read the shapes (subzones) and the grid of cells once
subzones = pd.read_csv('../share_data/aggregated_trips.csv')

# keep only relevant columns but preserve the geometry column so the result stays a
# GeoDataFrame (needed for GeoPandas methods like `to_file`).
cols = ["ORIGIN_SUBZONE", "DESTINATION_SUBZONE", "COUNT"]
result = []

for _, row in subzones.iterrows():
        result.append({
                        "origin_cell": row["ORIGIN_SUBZONE"],
                        "destination_cell": row["DESTINATION_SUBZONE"],
                        "in_amount": row["COUNT"]
                })
        
# Convert results to a plain CSV (no geometry)
if len(result) == 0:
    print("No flows generated.")
else:
    df_res = pd.DataFrame(result)
    out_path = "all_flow_cell3.csv"
    df_res.to_csv(out_path, index=False)
    print(f"Wrote {out_path} with {len(df_res)} records")