import pandas as pd
import geopandas as gpd

# Load the dataset
# Replace 'your_data.csv' with the actual filename
df = pd.read_csv('../share_data/aggregated_trips.csv')

print(df['COUNT'].sum())

gdf = pd.read_csv('./all_flow_cell.csv')
print(gdf['in_amount'].sum())

