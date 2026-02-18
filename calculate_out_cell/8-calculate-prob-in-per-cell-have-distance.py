import math
import geopandas as gpd
from shapely import Point

geojson_file2 = "final_summed_out_cells.geojson"
out_data = gpd.read_file(geojson_file2)

geojson_file = "categorized_cell_pairs.geojson"
pair_cell_gdf = gpd.read_file(geojson_file)

# 1. Load your GeoJSON
gdf = gpd.read_file('seoul_prob_pois.geojson')

# Ensure 'in_prob' column exists
pair_cell_gdf['in_prob'] = 0.0

def mobility_decay_probability(d, beta=1):
    return math.exp(-beta * d)

public_transport = 1.5
shop = 1.0
amenity = 1.0
office = 0.8
tourism= 0.8
othercase = 0.1

# Extract the first cell_id as a scalar value (not a Series)
for index1, row1 in gdf.iterrows():
    first_cell_id = row1["cell_id"]  # row1["cell_id"] is already a scalar, no need for .iloc[0]
    # print(f"First cell ID: {first_cell_id}")

    # Now filter using the scalar value
    all_pairs_under_1 = pair_cell_gdf[(pair_cell_gdf["cell_id"] == first_cell_id) & (pair_cell_gdf["category"] == "under_1km")]
   
    all_pairs_over_1 = pair_cell_gdf[(pair_cell_gdf["cell_id"] == first_cell_id) & (pair_cell_gdf["category"] == "1km-10km")]
   
    sum_pois = 0

    for index, row in all_pairs_under_1.iterrows():
        distance = row["distance_m"]
        pois_data = out_data[out_data["cell_id"] == row["cell_id"]].iloc[0]
        sum_pois += (othercase + float(pois_data["tourism"]) * tourism + float(pois_data["office"]) * office + float(pois_data["shop"]) * shop + float(pois_data["amenity"]) * amenity + float(pois_data["public_transport"]) * public_transport) * mobility_decay_probability(distance/1000)

    for index, row in all_pairs_under_1.iterrows():
        distance = row["distance_m"]
        pois_data = out_data[out_data["cell_id"] == row["cell_id"]].iloc[0]
        pois_right = (othercase + float(pois_data["tourism"]) * tourism + float(pois_data["office"]) * office + float(pois_data["shop"]) * shop + float(pois_data["amenity"]) * amenity + float(pois_data["public_transport"]) * public_transport) * mobility_decay_probability(distance/1000)
        pair_cell_gdf.at[index, "in_prob"] = pois_right/sum_pois * float(pois_data["prob_0"])

    sum_pois2 = 0

    for index, row in all_pairs_over_1.iterrows():
        distance = row["distance_m"]
        pois_data = out_data[out_data["cell_id"] == row["cell_id"]].iloc[0]
        sum_pois2 += (othercase + float(pois_data["tourism"]) * tourism + float(pois_data["office"]) * office + float(pois_data["shop"]) * shop + float(pois_data["amenity"]) * amenity + float(pois_data["public_transport"]) * public_transport) * mobility_decay_probability(distance/1000)

    for index, row in all_pairs_over_1.iterrows():
        distance = row["distance_m"]
        pois_data = out_data[out_data["cell_id"] == row["cell_id"]].iloc[0]
        pois_right = (othercase + float(pois_data["tourism"]) * tourism + float(pois_data["office"]) * office + float(pois_data["shop"]) * shop + float(pois_data["amenity"]) * amenity + float(pois_data["public_transport"]) * public_transport) * mobility_decay_probability(distance/1000)
        pair_cell_gdf.at[index, "in_prob"] = pois_right/sum_pois2 * float(pois_data["prob_10"])

pair_cell_gdf.to_file(geojson_file, driver='GeoJSON')