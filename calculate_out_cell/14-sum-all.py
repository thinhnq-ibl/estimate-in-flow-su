import pandas as pd
import geopandas as gdp

# Load the dataset
# Replace 'your_data.csv' with the actual filename
df = pd.read_csv('./all_flow_cell.csv')

print(df['in_amount'].sum())

df = pd.read_csv('./aggregated_origin_counts.csv')

print(df['COUNT'].sum())

df = gdp.read_file("./amount_out_from_cell.geojson")

print(df["final_out_value"].sum())

df = gdp.read_file("./final_summed_out_cells.geojson")

print(df["final_out_value"].sum())

geojson_file = "categorized_cell_pairs.geojson"

df = gdp.read_file(geojson_file)

print(df["in_amount"].sum())