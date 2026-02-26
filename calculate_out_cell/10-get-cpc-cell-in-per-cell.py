import geopandas as gpd
import pandas as pd

csv_data = "../share_data/aggregated_trips.csv"

csv_ob = pd.read_csv(csv_data)

geojson_file = "cells_split_by_rings.csv"
pair_cell_gdf = pd.read_csv(geojson_file)

gdf = gpd.read_file("amount_out_from_cell.geojson")

out_path = "all_flow_cell3.csv"

result = []

for _, flow in csv_ob.iterrows():
    # origin_zone and destination_zone are integers, not tuples
    origin_zone = flow["ORIGIN_SUBZONE"]
    destination_zone = flow["DESTINATION_SUBZONE"]
    origin_cells = gdf[gdf["SUBZONE_C"] == origin_zone]
    destination_cells = gdf[gdf["SUBZONE_C"] == destination_zone]

    total = 0

    for _, row1 in origin_cells.iterrows():
        for _, row2 in destination_cells.iterrows():
            # skip if already computed in existing output
            pair = pair_cell_gdf[
                (pair_cell_gdf["source_cell"] == row1["cell_id"]) &
                (pair_cell_gdf["neighbor_cell"] == row2["cell_id"])
            ]
            if pair.shape[0] > 0:
                total += pair.iloc[0]["in_amount"]

    print("total", total)

    result.append({
        # keep the original zone values as ints
        "origin_cell": int(origin_zone),
        "destination_cell": int(destination_zone),
        "in_amount": float(total)
    })

# Convert results to a plain CSV (no geometry)
if not result:
    print("No flows generated.")
else:
    df_res = pd.DataFrame(result)
    # append new rows to existing file (overwrite with combined data)
    df_res.to_csv(out_path, index=False)
    print(f"Wrote {out_path} with {len(df_res)} records")


