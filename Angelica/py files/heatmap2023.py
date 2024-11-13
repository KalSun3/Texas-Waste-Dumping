from folium.plugins import HeatMap
import pandas as pd
import folium
from branca.element import Template, MacroElement

# Load data from the provided CSV file
file_path = "CleanedFiles/2023_tx_cleaned.csv"  # Path to the uploaded CSV file
all_data = pd.read_csv(file_path)

# Verify that the CSV file has the expected columns
all_data.rename(columns={
    'LATITUDE': 'LATITUDE',
    'LONGITUDE': 'LONGITUDE',
    'TOTAL_RELEASES': 'TOTAL_RELEASES'
}, inplace=True)

# Filter data to include only rows with valid latitude, longitude, and total waste
heat_data = all_data[['LATITUDE', 'LONGITUDE', 'TOTAL_RELEASES']].dropna()

# Create a base map centered around Texas
m = folium.Map(location=[31.0, -99.0], zoom_start=6)

# Prepare data for the heatmap, weighted by `TOTAL_RELEASES`
heat_data = [[row['LATITUDE'], row['LONGITUDE'], row['TOTAL_RELEASES']] for index, row in heat_data.iterrows()]

# Add the heatmap layer
HeatMap(heat_data, radius=15, max_opacity=0.7).add_to(m)

# Add a customized legend to the map
legend_html = '''
  <div style="
  position: fixed;
  bottom: 50px;
  left: 50px;
  width: 220px;
  height: 120px;
  background-color: white;
  border: 2px solid grey;
  z-index: 9999;
  font-size: 14px;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
  line-height: 1.8;
  ">
    <strong>Waste Release Intensity</strong><br>
    <div style="margin-top: 10px;">
        <span style="display: inline-block; width: 20px; height: 12px; background-color: #ff0000; margin-right: 8px;"></span> High<br>
        <span style="display: inline-block; width: 20px; height: 12px; background-color: #ffa500; margin-right: 8px;"></span> Medium<br>
        <span style="display: inline-block; width: 20px; height: 12px; background-color: #ffff00; margin-right: 8px;"></span> Low<br>
    </div>
  </div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save map to HTML
m.save("total_releases_heatmap_2023.html")
print("Map has been created and saved as 'total_releases_heatmap_2023.html'. Open this file to view the map.")
