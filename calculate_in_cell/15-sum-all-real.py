import pandas as pd
import geopandas as gpd

# Load the dataset
# Replace 'your_data.csv' with the actual filename
df = pd.read_csv('../share_data/aggregated_trips.csv')

print(df['COUNT'].sum())

gdf = gpd.read_file('./map_zone_cell.geojson')
print(gdf['final_out_value'].sum())

