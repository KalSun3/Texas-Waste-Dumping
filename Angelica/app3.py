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
required_columns = {'FACILITY_NAME', 'YEAR', 'LATITUDE', 'LONGITUDE', 'TOTAL_RELEASES', 'CHEMICAL'}
if not required_columns.issubset(all_data.columns):
    raise ValueError("Data must contain the columns: 'FACILITY_NAME', 'YEAR', 'LATITUDE', 'LONGITUDE', 'TOTAL_RELEASES', and 'CHEMICAL'.")

# Debug: Check for missing values by year
print("Missing values by year:")
print(all_data.groupby('YEAR')[['FACILITY_NAME', 'TOTAL_RELEASES', 'LATITUDE', 'LONGITUDE', 'CHEMICAL']].apply(lambda x: x.isnull().sum()))

# Debug: Print sample data for a specific year, like 2009
print("Sample data for the year 2009:")
print(all_data[all_data['YEAR'] == 2009].head())

# Group data by facility name, year, and chemical, aggregating the total waste released for each year per facility and chemical
facility_chemical_year_data = all_data.groupby(['FACILITY_NAME', 'YEAR', 'CHEMICAL']).agg(
    total_waste=('TOTAL_RELEASES', 'sum'),
    latitude=('LATITUDE', 'first'),
    longitude=('LONGITUDE', 'first')
).reset_index()

# Debug: Check grouped data to verify multiple years and chemicals
print("Sample of grouped data (20 rows):")
print(facility_chemical_year_data.head(20))

# Create a folium map centered around Texas with a zoom level suitable for an overview
map_center = [31.0, -99.0]  # Texas approximate center
m = folium.Map(location=map_center, zoom_start=6)

# Use MarkerCluster to handle overlapping markers
marker_cluster = MarkerCluster().add_to(m)

# Define color mapping for chemicals
chemical_colors = {
    'Toluene': 'blue',
    'Methanol': 'green',
    'Benzene': 'red',
    'Xylene (mixed isomers)': 'purple',
    'Copper': 'orange',
    # Add more chemicals and colors as needed
}

# Add markers with popup to display facility name, year, chemical, and total waste
for _, row in facility_chemical_year_data.iterrows():
    # Get the color based on the chemical, default to gray if not in color mapping
    color = chemical_colors.get(row['CHEMICAL'], 'gray')

    # Popup content with facility name, year, chemical, and waste details
    popup_text = f"<strong>Facility:</strong> {row['FACILITY_NAME']}<br>" \
                 f"<strong>Year:</strong> {int(row['YEAR'])}<br>" \
                 f"<strong>Chemical:</strong> {row['CHEMICAL']}<br>" \
                 f"<strong>Total Waste Released:</strong> {row['total_waste']} lbs"
    
    # Add each marker to the marker cluster with specific color based on chemical
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_text,
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(marker_cluster)

# Save the map to an HTML file and display it
m.save("interactive_map_chemical_waste.html")
print("Map has been created and saved as 'interactive_map_chemical_waste.html'. Open this file to view the map.")
