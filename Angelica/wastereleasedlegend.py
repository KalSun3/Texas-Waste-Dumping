import json
import folium
import pandas as pd
from folium.plugins import MarkerCluster
from folium import FeatureGroup, LayerControl
from branca.element import Template, MacroElement

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

# Create a folium map centered around Texas
map_center = [31.0, -99.0]  # Texas approximate center
m = folium.Map(location=map_center, zoom_start=6)

# Define color scale for different ranges of waste intensity
def get_marker_color(total_waste):
    if total_waste < 500:
        return 'green'
    elif total_waste < 2000:
        return 'orange'
    else:
        return 'red'

# Create a feature group for each year and add markers
years = county_year_data['YEAR'].unique()
for year in years:
    # Create a feature group for the specific year
    year_group = FeatureGroup(name=f"{year} Waste Releases")
    # Filter data for the specific year
    year_data = county_year_data[county_year_data['YEAR'] == year]
    
    # Use MarkerCluster to manage overlapping markers
    marker_cluster = MarkerCluster().add_to(year_group)
    
    for _, row in year_data.iterrows():
        # Determine color based on total waste
        color = get_marker_color(row['total_waste'])
        
        # Popup content with county, year, and waste details
        popup_text = f"<strong>County:</strong> {row['COUNTY']}<br>" \
                     f"<strong>Year:</strong> {int(row['YEAR'])}<br>" \
                     f"<strong>Total Waste Released:</strong> {row['total_waste']} lbs"
        
        # Add marker to the cluster with color and popup info
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_text,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(marker_cluster)
    
    # Add year group to map
    year_group.add_to(m)

# Add a layer control panel to toggle year layers on/off
LayerControl().add_to(m)

# Add a legend for waste intensity colors
legend_html = '''
<div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 180px;
    background-color: white;
    border:2px solid grey;
    z-index:9999;
    font-size:14px;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    line-height: 1.5;
    ">
    <strong>Waste Release Intensity</strong><br>
    <div style="margin-top: 8px;">
        <span style="display: inline-block; width: 20px; height: 12px; background-color: green; margin-right: 8px;"></span> Low (< 500 lbs)<br>
        <span style="display: inline-block; width: 20px; height: 12px; background-color: orange; margin-right: 8px;"></span> Medium (500-2000 lbs)<br>
        <span style="display: inline-block; width: 20px; height: 12px; background-color: red; margin-right: 8px;"></span> High (> 2000 lbs)
    </div>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file and display it
m.save("interactive_waste_release_map_with_legend_and_layers.html")
print("Map has been created and saved as 'interactive_waste_release_map_with_legend_and_layers.html'. Open this file to view the map.")
