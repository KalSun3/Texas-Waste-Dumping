import json
import folium
import pandas as pd
from folium.plugins import HeatMapWithTime

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
required_columns = {'FACILITY_NAME', 'YEAR', 'LATITUDE', 'LONGITUDE', 'TOTAL_RELEASES'}
if not required_columns.issubset(all_data.columns):
    raise ValueError("Data must contain the columns: 'FACILITY_NAME', 'YEAR', 'LATITUDE', 'LONGITUDE', and 'TOTAL_RELEASES'.")

# Prepare data for each year for the time-lapse
heat_data_time = []
years = sorted(all_data['YEAR'].unique())  # Sorted list of unique years

for year in years:
    # Filter data for the specific year and drop rows with NaN values in required columns
    year_data = all_data[(all_data['YEAR'] == year) & all_data[['LATITUDE', 'LONGITUDE', 'TOTAL_RELEASES']].notnull().all(axis=1)]
    
    # Create the data format for the heatmap with time: [[latitude, longitude, intensity], ...]
    heat_data_year = [[row['LATITUDE'], row['LONGITUDE'], row['TOTAL_RELEASES']] for index, row in year_data.iterrows()]
    
    # Add this year's data to the heat_data_time list
    heat_data_time.append(heat_data_year)

# Create a base map centered around Texas with a zoom level suitable for an overview
map_center = [31.0, -99.0]  # Texas approximate center
m = folium.Map(location=map_center, zoom_start=6)

# Add time-lapse heatmap to the map
HeatMapWithTime(
    heat_data_time,  # Data prepared for each year
    radius=15,       # Radius of each heat point
    max_opacity=0.8, # Max opacity of heat points
    gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}  # Gradient from low to high intensity
).add_to(m)

# Save the map to an HTML file and display it
m.save("time_lapse_heatmap.html")
print("Time-lapse map has been created and saved as 'time_lapse_heatmap.html'. Open this file to view the animated map.")
