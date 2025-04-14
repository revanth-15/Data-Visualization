import pandas as pd
import json

# Load dataset
df = pd.read_csv("region_01.csv")

# Remove unknown or missing group names
df = df[df['gname'].notna()]
df = df[df['gname'] != 'Unknown']

# Group and count incidents by year and group
grouped = df.groupby(['iyear', 'gname']).size().reset_index(name='incidents')

# Build nested dictionary: {year: [{group, count}, ...]}
result = {}
for year in grouped['iyear'].unique():
    top_groups = grouped[grouped['iyear'] == year].sort_values(by='incidents', ascending=False).head(10)
    result[str(year)] = [
        {"group": row['gname'], "count": int(row['incidents'])}
        for _, row in top_groups.iterrows()
    ]

# Save to JSON
with open("top_groups_by_year.json", "w") as f:
    json.dump(result, f, indent=2)

print(" top_groups_by_year.json generated successfully!")
