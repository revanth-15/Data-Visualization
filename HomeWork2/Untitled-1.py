import pandas as pd # Import the pandas library
import geopandas as gpd # Import the geopandas library
import folium # Import the folium library
from folium.plugins import HeatMap # Import the HeatMap plugin
import matplotlib.pyplot as plt # Import the matplotlib library
import seaborn as sns # Import the seaborn library
from statsmodels.tsa.seasonal import seasonal_decompose # Import the seasonal_decompose function

# Load the dataset
file_path = 'terrorism_incident.csv'  # Correct file path

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, encoding='ISO-8859-1')  # Read the CSV correctly

# Data Cleaning: Remove rows with missing latitude or longitude
df_cleaned = df.dropna(subset=['latitude', 'longitude']) # Drop rows with missing latitude or longitude

# Ensure there are valid coordinates before proceeding
if df_cleaned.empty: # Check if the cleaned DataFrame is empty
    raise ValueError("No valid latitude/longitude data available for analysis.") # Raise an error if no valid data

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(
    df_cleaned, geometry=gpd.points_from_xy(df_cleaned.longitude, df_cleaned.latitude), crs='EPSG:4326'
) # Convert the cleaned DataFrame to a GeoDataFrame with point geometries

# Display the first few rows of the GeoDataFrame
print(gdf.head()) # Print the first few rows of the GeoDataFrame

# Summary statistics of numerical columns
summary_stats = gdf.describe() # Get summary statistics of numerical columns
print("Summary Statistics:") # Print a label for the summary statistics
print(summary_stats) # Print the summary statistics

# Simple plot using GeoPandas' built-in functionality
gdf.plot(figsize=(10, 6), alpha=0.5, edgecolor='k') # Plot the GeoDataFrame
plt.title("Terrorism Incidents Distribution") # Set the title of the plot
plt.show() # Show the plot

# ---- Geospatial Visualization ---- #

# Creating a base map with markers
base_map = folium.Map(location=[df_cleaned['latitude'].mean(), df_cleaned['longitude'].mean()], zoom_start=2) # Create a base map centered on the mean latitude and longitude
for _, row in df_cleaned.iterrows(): # Iterate over the rows of the cleaned DataFrame
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']], # Set the location of the marker
        radius=2, # Set the radius of the marker
        color='red', # Set the color of the marker
        fill=True, # Enable filling the marker
        fill_color='red', # Set the fill color of the marker
        fill_opacity=0.5, # Set the fill opacity of the marker
        popup=row['city'] # Set the popup text to the city name
    ).add_to(base_map) # Add the marker to the base map
base_map.save("base_map.html") # Save the base map to an HTML file

# Choropleth Map (Incidents per Country)
country_counts = df['country_txt'].value_counts().reset_index() # Get the count of incidents per country
country_counts.columns = ['country_txt', 'count'] # Rename the columns
choropleth_map = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=2) # Create a base map centered on the mean latitude and longitude
folium.Choropleth(
    geo_data='https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json', # URL to the GeoJSON file
    data=country_counts, # Data for the choropleth map
    columns=['country_txt', 'count'], # Columns to use for the choropleth map
    key_on='feature.properties.name', # Key to match the GeoJSON data with the DataFrame
    fill_color='YlOrRd', # Color scheme for the choropleth map
    fill_opacity=0.7, # Fill opacity for the choropleth map
    line_opacity=0.2, # Line opacity for the choropleth map
    legend_name='Terrorism Incidents per Country' # Legend name for the choropleth map
).add_to(choropleth_map) # Add the choropleth layer to the map
choropleth_map.save("choropleth_map.html") # Save the choropleth map to an HTML file

# Creating a heatmap of incidents
heatmap = folium.Map(location=[df_cleaned['latitude'].mean(), df_cleaned['longitude'].mean()], zoom_start=2) # Create a base map centered on the mean latitude and longitude
HeatMap(df_cleaned[['latitude', 'longitude']].values, radius=10).add_to(heatmap) # Add a heatmap layer to the map
heatmap.save("heatmap.html") # Save the heatmap to an HTML file

# Top 5 attack types
attack_counts = df_cleaned['attacktype1_txt'].value_counts().head(5) # Get the top 5 attack types

# Pie chart
plt.figure(figsize=(8, 6)) # Create a new figure for the pie chart
attack_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='coolwarm') # Plot the pie chart
plt.title("Top 5 Attack Types") # Set the title of the pie chart
plt.ylabel('') # Remove the y-axis label
plt.show() # Show the pie chart

# Bar chart
plt.figure(figsize=(10, 5)) # Create a new figure for the bar chart
sns.barplot(x=attack_counts.index, y=attack_counts.values, palette='viridis') # Plot the bar chart
plt.title("Frequency of Top 5 Attack Types") # Set the title of the bar chart
plt.xlabel("Attack Type") # Set the x-axis label
plt.ylabel("Count") # Set the y-axis label
plt.xticks(rotation=45) # Rotate the x-axis labels
plt.show() # Show the bar chart
print("Top 5 Attack Types Frequency:") # Print a label for the attack type frequencies
print(attack_counts) # Print the attack type frequencies

# Number of incidents per year
yearly_incidents = df_cleaned.groupby('iyear').size() # Group the data by year and count the number of incidents

# Line plot of incidents per year
plt.figure(figsize=(12, 6)) # Create a new figure for the line plot
plt.plot(yearly_incidents.index, yearly_incidents.values, marker='o', linestyle='-') # Plot the line plot
plt.title("Terrorism Incidents per Year") # Set the title of the line plot
plt.xlabel("Year") # Set the x-axis label
plt.ylabel("Number of Incidents") # Set the y-axis label
plt.grid() # Enable the grid
plt.show() # Show the line plot

# Time series decomposition
try:
    decomposed = seasonal_decompose(yearly_incidents, model='additive', period=5)  # Adjusted period
    # Plot decomposition results
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True) # Create subplots for the decomposition results
    decomposed.trend.plot(ax=axes[0], title='Trend') # Plot the trend component
    decomposed.seasonal.plot(ax=axes[1], title='Seasonality') # Plot the seasonal component
    decomposed.resid.plot(ax=axes[2], title='Residuals') # Plot the residual component
    plt.xlabel("Year")  # Label the x-axis with 'Year'
    plt.show() # Show the decomposition plots
except ValueError: # Handle the case where there are not enough data points
    print("Not enough data points for seasonal decomposition. Consider increasing dataset size.") # Print an error message
