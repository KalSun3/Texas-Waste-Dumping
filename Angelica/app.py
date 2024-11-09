import json
import folium
import pandas as pd
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

# Ensure required columns
required_columns = {'COUNTY', 'YEAR', 'LATITUDE', 'LONGITUDE', 'TOTAL_RELEASES'}
if not required_columns.issubset(all_data.columns):
    raise ValueError("Data must contain the columns: 'COUNTY', 'YEAR', 'LATITUDE', 'LONGITUDE', and 'TOTAL_RELEASES'.")

# Group data by county and year, aggregating the total waste released for each year per county
county_year_data = all_data.groupby(['COUNTY', 'YEAR']).agg(
    total_waste=('TOTAL_RELEASES', 'sum'),
    latitude=('LATITUDE', 'first'),
    longitude=('LONGITUDE', 'first')
).reset_index()

# Create a folium map centered around Texas with a zoom level suitable for an overview
map_center = [31.0, -99.0]  # Texas approximate center
m = folium.Map(location=map_center, zoom_start=6)

# Use MarkerCluster to handle overlapping markers
marker_cluster = MarkerCluster().add_to(m)

# Add markers with popup to display county name, year, and total waste
for _, row in county_year_data.iterrows():
    # Popup content with county, year, and waste details
    popup_text = f"<strong>County:</strong> {row['COUNTY']}<br>" \
                 f"<strong>Year:</strong> {int(row['YEAR'])}<br>" \
                 f"<strong>Total Waste Released:</strong> {row['total_waste']} lbs"
    
    # Ensure each marker is added only to the cluster, not as a standalone marker
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_text
    ).add_to(marker_cluster)

# Save the map to an HTML file and display it
m.save("interactive_map.html")
print("Map has been created and saved as 'interactive_map.html'. Open this file to view the map.")
