import json
import folium
import pandas as pd
from folium.plugins import MarkerCluster
from folium import FeatureGroup, LayerControl

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

# Create layers for each year and add to map
unique_years = county_year_data['YEAR'].unique()
for year in unique_years:
    year_data = county_year_data[county_year_data['YEAR'] == year]
    year_layer = FeatureGroup(name=str(year))  # Layer for each year

    for _, row in year_data.iterrows():
        # Set color and radius based on total waste level
        total_waste = row['total_waste']
        color = 'green' if total_waste < 500 else 'yellow' if total_waste < 2000 else 'orange' if total_waste < 5000 else 'red'
        radius = max(5, min(total_waste / 500, 15))  # Limits radius between 5 and 15

        # Popup content with county, year, and waste details
        popup_text = f"<strong>County:</strong> {row['COUNTY']}<br>" \
                     f"<strong>Year:</strong> {int(row['YEAR'])}<br>" \
                     f"<strong>Total Waste Released:</strong> {row['total_waste']} lbs"

        # Add circle marker with popup
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.4,  # Adjust opacity for better clarity
            popup=popup_text
        ).add_to(year_layer)

    # Add each year's layer to the map
    year_layer.add_to(m)

# Add layer control to toggle layers by year
LayerControl().add_to(m)

# Save the map to an HTML file and display it
m.save("enhanced_interactive_map.html")
print("Enhanced map has been created and saved as 'enhanced_interactive_map.html'. Open this file to view the map.")
