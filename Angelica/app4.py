from folium.plugins import HeatMap
import json
import pandas as pd
import folium
from branca.element import Template, MacroElement

# Load data from JSON files
files = ["data_9_to_11.json", "data_12_to_14.json", "data_15_to_17.json", "data_18_to_20.json", "data_21_to_23.json"]
all_data = pd.DataFrame()
for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        all_data = pd.concat([all_data, df], ignore_index=True)

# Filter data to include only rows with valid latitude, longitude, and total waste
heat_data = all_data[['LATITUDE', 'LONGITUDE', 'TOTAL_RELEASES']].dropna()

# Create a base map centered around Texas
m = folium.Map(location=[31.0, -99.0], zoom_start=6)

# Prepare data for the heatmap, weighted by `TOTAL_RELEASES`
heat_data = [[row['LATITUDE'], row['LONGITUDE'], row['TOTAL_RELEASES']] for index, row in heat_data.iterrows()]

# Add the heatmap layer
HeatMap(heat_data, radius=15, max_opacity=0.7).add_to(m)

# Add legend to the map
legend_html = '''
  <div style="
  position: fixed;
  bottom: 50px;
  left: 50px;
  width: 200px;
  height: 90px;
  background-color: white;
  border:2px solid grey;
  z-index:9999;
  font-size:14px;
  padding: 10px;
  ">&nbsp; Waste Release Intensity <br>
    &nbsp; <i style="background: #ff0000; width: 10px; height: 10px; display: inline-block;"></i>&nbsp; High<br>
    &nbsp; <i style="background: #ffa500; width: 10px; height: 10px; display: inline-block;"></i>&nbsp; Medium<br>
    &nbsp; <i style="background: #ffff00; width: 10px; height: 10px; display: inline-block;"></i>&nbsp; Low<br>
  </div>
  '''
m.get_root().html.add_child(folium.Element(legend_html))

# Save map to HTML
m.save("total_releases_heatmap.html")
print("Map has been created and saved as 'total_releases_heatmap.html'. Open this file to view the map.")
