import json
import pandas as pd
import geopandas as gpd

# Giả sử data_geojson là biến chứa nội dung bạn vừa gửi
def convert_to_od_pairs(df, geographic_crs='EPSG:4326'):
    rows = []
    for index, row in df.iterrows():
        # Giả sử gdf là GeoDataFrame bạn đã load từ GeoJSON
        # 1. Lấy tâm của các Polygon
        centroids = row.geometry.centroid

        # Transform centroid to geographic CRS to get lat/lng
        centroids_geo = gpd.GeoSeries([centroids], crs=df.crs).to_crs(geographic_crs).iloc[0]
        centroid_lng = centroids_geo.x
        centroid_lat = centroids_geo.y
        
        # Giả định: 
        # Left là Origin (Điểm đi), Right là Destination (Điểm đến)
        # Tọa độ thực tế cần lấy từ tâm của mỗi cell (ở đây lấy tạm tâm Polygon hiện tại)
        rows.append({
            'origin_id': row['cell_id'],
            'pop_count': row['pop_count'],
            'district_name': row['district_name'],
            'origin_lat': centroid_lat, # Bạn nên thay bằng tâm thực của cell_left
            'origin_lng': centroid_lng, # Bạn nên thay bằng tâm thực của cell_left
            'flow_volume': row['norm_in_amount'],
        })
    
    return pd.DataFrame(rows)

# 1. Load the GeoJSON file
# Ensure 'hcmc_pop_grid.geojson' is in your current directory
file_path = "in_flow_cells_normalized.geojson"
gdf = gpd.read_file(file_path)

# hcm_file_path = "hcmc_pop_grid.geojson"
# hcm_gdf = gpd.read_file(hcm_file_path)

# Reproject to projected CRS for accurate centroid calculation
projected_crs = 'EPSG:32648'  # UTM zone 48N for Vietnam
gdf_projected = gdf.to_crs(projected_crs)

df = convert_to_od_pairs(gdf_projected)
df.to_csv('in_flow_cells_normalized.csv', index=False)