import pandas as pd
import json

# Load dataset
df = pd.read_csv("region_01.csv")

# Aggregate by year and attack type
attack_data = df.groupby(['iyear', 'attacktype1_txt']).size().reset_index(name='count')

# Convert to a dictionary for Plotly
result = {}
for year in attack_data['iyear'].unique():
    yearly_data = attack_data[attack_data['iyear'] == year]
    result[str(year)] = [
        {"attack_type": row['attacktype1_txt'], "count": int(row['count'])}
        for _, row in yearly_data.iterrows()
    ]

# Save to JSON
with open("attack_types_by_year.json", "w") as f:
    json.dump(result, f, indent=2)

print(" attack_types_by_year.json generated successfully!")
