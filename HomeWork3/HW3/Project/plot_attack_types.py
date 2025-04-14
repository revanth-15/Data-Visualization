import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

#  Read the dataset
df = pd.read_csv('region_01.csv')

#  Keep only required columns
req_cols = [
    "iyear", "imonth", "iday", "country_txt",
    "region_txt", "city", "latitude", "longitude",
    "attacktype1_txt", "nkill", "nwound"
]

df = df[req_cols]

# : Handle missing values
df['latitude'] = df.groupby('city')['latitude'].transform(lambda x: x.fillna(x.median()))
df['longitude'] = df.groupby('city')['longitude'].transform(lambda x: x.fillna(x.median()))
df[['nkill', 'nwound']] = df[['nkill', 'nwound']].fillna(0)

#  Aggregate attack types by year
attack_types_by_year = df.groupby(['iyear', 'attacktype1_txt']).size().reset_index(name='count')

# Pivot data for stacked area chart
pivoted_data = attack_types_by_year.pivot(
    index='iyear', 
    columns='attacktype1_txt', 
    values='count'
).fillna(0)

#  Normalize data for 100% stacked view
def normalize_data(data):
    return data.div(data.sum(axis=1), axis=0)

pivoted_data_normalized = normalize_data(pivoted_data)

#  Create figure with subplots for different view modes
fig = go.Figure()

#  Add traces for regular stacked chart
for attack_type in pivoted_data.columns:
    fig.add_trace(go.Scatter(
        x=pivoted_data.index,
        y=pivoted_data[attack_type],
        mode='lines',
        stackgroup='one',
        name=attack_type,
        visible=True
    ))

#  Add traces for 100% stacked chart (normalized)
for attack_type in pivoted_data_normalized.columns:
    fig.add_trace(go.Scatter(
        x=pivoted_data_normalized.index,
        y=pivoted_data_normalized[attack_type],
        mode='lines',
        stackgroup='one',
        name=attack_type,
        visible=False
    ))

#  Add traces for grouped mode (no stacking)
for attack_type in pivoted_data.columns:
    fig.add_trace(go.Scatter(
        x=pivoted_data.index,
        y=pivoted_data[attack_type],
        mode='lines',
        name=attack_type,
        visible=False
    ))

#  Update layout with buttons to toggle between modes
fig.update_layout(
    title="Attack Types Over Time",
    title_x=0.5,
    title_y=1,
    title_pad=dict(t=40),
    xaxis_title="Year",
    yaxis_title="Number of Incidents",
    height=800,
    width=1200,
    margin={"l": 50, "r": 250, "t": 180, "b": 50},
    updatemenus=[  
        dict(
            type="buttons",
            direction="right",
            x=0.57,
            y=1.1,
            showactive=True,
            buttons=list([
                dict(label="Stacked",
                     method="update",
                     args=[{"visible": [True] * len(pivoted_data.columns) + [False] * len(pivoted_data_normalized.columns) + [False] * len(pivoted_data.columns)}]),
                dict(label="Grouped",
                     method="update",
                     args=[{"visible": [False] * len(pivoted_data.columns) + [False] * len(pivoted_data_normalized.columns) + [True] * len(pivoted_data.columns)}]),
                dict(label="100% Stacked",
                     method="update",
                     args=[{"visible": [False] * len(pivoted_data.columns) + [True] * len(pivoted_data_normalized.columns) + [False] * len(pivoted_data.columns)}]),
            ]),
        )
    ],
    legend=dict(
        x=1.1,
        y=1,
        traceorder="normal",
        orientation="v",
        font=dict(size=10),
        bordercolor="Black",
        borderwidth=1
    )
)

# Save the plot as an interactive HTML file
pio.write_html(fig, file='attack_types_chart.html', auto_open=False)

# Adjust HTML to change tab title
with open('attack_types_chart.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

html_content = html_content.replace('<title>Plotly</title>', '<title>Attack Types Chart</title>')

# Write the updated HTML content back to the file
with open('attack_types_chart.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Visualization saved as attack_types_chart.html")
