import pandas as pd
import json

# Load the CSV file
df = pd.read_csv("region_01.csv")

# Extract year and country
df_map = df[['iyear', 'country_txt']].copy()

# Count incidents by year and country
agg = df_map.groupby(['iyear', 'country_txt']).size().reset_index(name='incidents')

# Convert to nested dict: {year: {country: count}}
result = {}
for _, row in agg.iterrows():
    year = str(row['iyear'])
    country = row['country_txt']
    count = int(row['incidents'])

    if year not in result:
        result[year] = {}
    result[year][country] = count

# Save to JSON
with open("heatmap_data.json", "w") as f:
    json.dump(result, f)

print(" heatmap_data.json created successfully!")
