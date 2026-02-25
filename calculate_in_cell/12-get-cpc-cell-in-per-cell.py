import geopandas as gpd
import pandas as pd

df = pd.read_csv('../share_data/aggregated_trips.csv')
# avoid shadowing built-in `map`
map_gdf = gpd.read_file('./map_zone_cell.geojson')
result = []

for _, row in df.iterrows():
    origin_zone = row["ORIGIN_SUBZONE"]
    destination_zone = row["DESTINATION_SUBZONE"]
    origin_cells = map_gdf[map_gdf["SUBZONE_C"] == origin_zone]
    destination_cells = map_gdf[map_gdf["SUBZONE_C"] == destination_zone]
    for _, c in origin_cells.iterrows():
        out_total_amount = row["COUNT"]
        out_cell = out_total_amount * c["intersect_area_m2"] / c["group_area"]
            
        for _, c2 in destination_cells.iterrows():
            in_amount = out_cell * c2["intersect_area_m2"] / c2["group_area"]
                
            result.append({
                "origin_cell": c["cell_id"],
                "destination_cell": c2["cell_id"],
                "in_amount": in_amount
            })

# Convert results to a plain CSV (no geometry)
if len(result) == 0:
    print("No flows generated.")
else:
    df_res = pd.DataFrame(result)
    out_path = "all_flow_cell_detail.csv"
    df_res.to_csv(out_path, index=False)
    print(f"Wrote {out_path} with {len(df_res)} records")