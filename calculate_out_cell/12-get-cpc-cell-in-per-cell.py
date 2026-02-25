import geopandas as gpd
import pandas as pd

geojson_file = "categorized_cell_pairs.geojson"
pair_cell_gdf = gpd.read_file(geojson_file)

result = []

for _, row in pair_cell_gdf.iterrows():
    result.append({
        "origin_cell": row["cell_id"],
        "destination_cell": row["neighbor_id"],
        "in_amount": row ["in_amount"]
    })

# Convert results to a plain CSV (no geometry)
if len(result) == 0:
    print("No flows generated.")
else:
    df_res = pd.DataFrame(result)
    out_path = "all_flow_cell.csv"
    df_res.to_csv(out_path, index=False)
    print(f"Wrote {out_path} with {len(df_res)} records")