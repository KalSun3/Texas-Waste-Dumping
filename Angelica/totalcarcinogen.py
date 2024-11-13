import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster

# List of JSON files
files = ["data_9_to_11.json", "data_12_to_14.json", "data_15_to_17.json", "data_18_to_20.json", "data_21_to_23.json"]

# Initialize an empty DataFrame
all_data = pd.DataFrame()

# Load data from each JSON file and combine them
for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        all_data = pd.concat([all_data, df], ignore_index=True)

# Ensure the dataset contains required columns
required_columns = {'COUNTY', 'LATITUDE', 'LONGITUDE', 'CARCINOGEN', 'TOTAL_RELEASES'}
if not required_columns.issubset(all_data.columns):
    raise ValueError("Data must contain 'COUNTY', 'LATITUDE', 'LONGITUDE', 'CARCINOGEN', and 'TOTAL_RELEASES' columns.")

# Filter for carcinogenic releases
carcinogen_data = all_data[all_data['CARCINOGEN'] == 'YES']

# Group by county, summing up the total carcinogenic releases
county_carcinogen_data = carcinogen_data.groupby('COUNTY').agg(
    total_carcinogen_releases=('TOTAL_RELEASES', 'sum'),
    latitude=('LATITUDE', 'first'),
    longitude=('LONGITUDE', 'first')
).reset_index()

# Create a folium map centered around Texas
map_center = [31.0, -99.0]
m = folium.Map(location=map_center, zoom_start=6)

# Use MarkerCluster to handle overlapping markers
marker_cluster = MarkerCluster().add_to(m)

# Add markers with popup to display county and total carcinogenic waste released
for _, row in county_carcinogen_data.iterrows():
    popup_text = f"<strong>County:</strong> {row['COUNTY']}<br>" \
                 f"<strong>Total Carcinogenic Waste Released:</strong> {row['total_carcinogen_releases']} lbs"
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_text,
        icon=folium.Icon(color='red', icon="exclamation-sign")
    ).add_to(marker_cluster)

# Save map to HTML
m.save("total_carcinogen_releases_by_county.html")
print("Map has been created and saved as 'total_carcinogen_releases_by_county.html'. Open this file to view the map.")
