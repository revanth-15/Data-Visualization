from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Slider
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.palettes import Category20, Category20c
import pandas as pd

# Load dataset
df = pd.read_csv("region_01.csv")

# Clean and prepare
df = df[['iyear', 'targtype1_txt', 'nkill', 'nwound']].copy()
df['nkill'] = df['nkill'].fillna(0)
df['nwound'] = df['nwound'].fillna(0)
df['total'] = df['nkill'] + df['nwound']
df['targtype1_txt'] = df['targtype1_txt'].fillna('Unknown')

# Assign unique color to each target type
target_types = df['targtype1_txt'].unique()
palette = Category20[20] if len(target_types) <= 20 else Category20c[20]
color_map = {t: palette[i % len(palette)] for i, t in enumerate(target_types)}
df['color'] = df['targtype1_txt'].map(color_map)

# Initial setup
initial_year = df['iyear'].min()
filtered = df[df['iyear'] == initial_year]
source = ColumnDataSource(filtered)

# Create figure
p = figure(title="Target Types and Casualties", 
           x_axis_label='Number Killed', y_axis_label='Number Wounded', 
           width=800, height=500, tools="pan,wheel_zoom,reset")

# Plot with colors
p.circle('nkill', 'nwound', size='total', color='color', source=source,
         fill_alpha=0.6, legend_field='targtype1_txt')

# Hover tool
hover = HoverTool(tooltips=[
    ("Target", "@targtype1_txt"),
    ("Killed", "@nkill"),
    ("Wounded", "@nwound")
])
p.add_tools(hover)

# Customize legend
p.legend.label_text_font_size = "8pt"
p.legend.location = "top_right"

# Slider
slider = Slider(start=df['iyear'].min(), end=df['iyear'].max(), value=initial_year, step=1, title="Year")

def update(attr, old, new):
    year = slider.value
    new_data = df[df['iyear'] == year]
    source.data = ColumnDataSource.from_df(new_data)

slider.on_change('value', update)

layout = column(slider, p)

# Show in Bokeh server
curdoc().add_root(layout)
