#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bokeh.plotting import figure, output_file, show
## To run Bokeh plots in Jupyter, use output_notebook(). Otherwise use output_file('filename.html') to display in a html page
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.tools import HoverTool
from bokeh.palettes import Inferno5, Spectral3
from bokeh.transform import factor_cmap
from bokeh.models import BoxAnnotation
from bokeh.tile_providers import get_provider
from pyproj import Transformer
from bokeh.layouts import layout

import pandas as pd



output_file('thorwwii.html.')


# In[3]:


df = pd.read_csv("thor_wwii.csv")
df


# In[7]:


x = [1, 3, 5, 7]
y = [2, 4, 6, 8]


# In[ ]:





# In[12]:


p = figure()

p.circle(x, y, size=10, color='red', legend_label='circle')
p.line(x, y, color='blue', legend_label='line')
p.triangle(y, x, color='gold', size=10, legend_label='triangle')
##Allows user to show/hide plot on line by clicking legend
p.legend.click_policy='hide'


# In[13]:


show(p)


# In[29]:


colum = df.columns.tolist()
colum
#MSNDATE (mission date), NAF (numbered airforce responsible for mission), AC_ATTACKING (number of aircraft), TONS_HE (high-explosives), TONS_IC (incendiary devices), TONS_FRAG (fragmentation bombs).


# In[4]:


#sample = df.sample(50)
source = ColumnDataSource(df.sample(50))


p = figure()
p.circle(x = 'TOTAL_TONS', y = 'AC_ATTACKING',
        source = source,
        size = 'TONS_HE', color = 'green')

p.title.text = 'Attacking Aircraft and Munitions Dropped'
p.xaxis.axis_label = 'Tons of Munitions Dropped'
p.yaxis.axis_label = 'Number of Attacking Aircraft'

hover = HoverTool()
hover.tooltips=[
    ('Attack Date', '@MSNDATE'),
    ('Attacking Aircraft', '@AC_ATTACKING'),
    ('Tons of Munitions', '@TOTAL_TONS'),
    ('Type of Aircraft', '@AIRCRAFT_NAME')
]

p.add_tools(hover)

show(p)


# In[62]:


grouped = df.groupby('COUNTRY_FLYING_MISSION')[['TOTAL_TONS', 'TONS_HE', 'TONS_IC', 'TONS_FRAG']].sum()


# In[64]:


grouped = grouped / 1000


# In[65]:


source = ColumnDataSource(grouped)
countries = source.data['COUNTRY_FLYING_MISSION'].tolist()
p = figure(x_range=countries)


# In[75]:


color_map = factor_cmap(field_name='COUNTRY_FLYING_MISSION',
                    palette=Inferno5, factors=countries)

p.vbar(x='COUNTRY_FLYING_MISSION', top='TOTAL_TONS', source=source, width=0.70, color=color_map)

p.title.text ='Munitions Dropped by Allied Country'
p.xaxis.axis_label = 'Country'
p.yaxis.axis_label = 'Kilotons of Munitions'


# In[76]:


hover = HoverTool()
hover.tooltips = [
    ("Totals", "@TONS_HE High Explosive / @TONS_IC Incendiary / @TONS_FRAG Fragmentation")]

hover.mode = 'vline'

p.add_tools(hover)

show(p)


# In[79]:


filtr = df['COUNTRY_FLYING_MISSION'].isin(('USA','GREAT BRITAIN'))
df = df[filtr]


# In[81]:


grouped = df.groupby('COUNTRY_FLYING_MISSION')[['TONS_IC', 'TONS_FRAG', 'TONS_HE']].sum()

#convert tons to kilotons again
grouped = grouped / 1000


# In[83]:


source = ColumnDataSource(grouped)
countries = source.data['COUNTRY_FLYING_MISSION'].tolist()
p = figure(x_range=countries)


# In[85]:


p.vbar_stack(stackers=['TONS_HE', 'TONS_FRAG', 'TONS_IC'],
             x='COUNTRY_FLYING_MISSION', source=source,
             legend_label = ['High Explosive', 'Fragmentation', 'Incendiary'],
             width=0.5, color=Spectral3)


# In[86]:


p.title.text ='Types of Munitions Dropped by Allied Country'
p.legend.location = 'top_left'

p.xaxis.axis_label = 'Country'
p.xgrid.grid_line_color = None	#remove the x grid lines

p.yaxis.axis_label = 'Kilotons of Munitions'

show(p)


# In[90]:


df = pd.read_csv('thor_wwii.csv')

#make sure MSNDATE is a datetime format
df['MSNDATE'] = pd.to_datetime(df['MSNDATE'], format='%m/%d/%Y')

grouped = df.groupby('MSNDATE')[['TOTAL_TONS', 'TONS_IC', 'TONS_FRAG']].sum()
grouped = grouped/1000

source = ColumnDataSource(grouped)

p = figure(x_axis_type='datetime')

p.line(x='MSNDATE', y='TOTAL_TONS', line_width=2, source=source, legend_label='All Munitions')
p.line(x='MSNDATE', y='TONS_FRAG', line_width=2, source=source, color=Spectral3[1], legend_label='Fragmentation')
p.line(x='MSNDATE', y='TONS_IC', line_width=2, source=source, color=Spectral3[2], legend_label='Incendiary')

p.yaxis.axis_label = 'Kilotons of Munitions Dropped'

show(p)


# In[93]:


grouped = df.groupby(pd.Grouper(key='MSNDATE', freq='M'))[['TOTAL_TONS', 'TONS_IC', 'TONS_FRAG']].sum()

grouped = grouped/1000

source = ColumnDataSource(grouped)

p = figure(x_axis_type='datetime')

p.line(x='MSNDATE', y='TOTAL_TONS', line_width=2, source=source, legend_label='All Munitions')
p.line(x='MSNDATE', y='TONS_FRAG', line_width=2, source=source, color=Spectral3[1], legend_label='Fragmentation')
p.line(x='MSNDATE', y='TONS_IC', line_width=2, source=source, color=Spectral3[2], legend_label='Incendiary')

p.yaxis.axis_label = 'Kilotons of Munitions Dropped'

show(p)


# In[101]:


df = pd.read_csv('thor_wwii.csv')

#filter for the European Theater of Operations
filtr = df['THEATER']=='ETO'
df = df[filtr]

df['MSNDATE'] = pd.to_datetime(df['MSNDATE'], format='%m/%d/%Y')
group = df.groupby(pd.Grouper(key='MSNDATE', freq='M'))[['TOTAL_TONS', 'TONS_IC', 'TONS_FRAG']].sum()
group = group / 1000

source = ColumnDataSource(group)

p = figure(x_axis_type="datetime")

p.line(x='MSNDATE', y='TOTAL_TONS', line_width=2, source=source, legend_label='All Munitions')
p.line(x='MSNDATE', y='TONS_FRAG', line_width=2, source=source, color=Spectral3[1], legend_label='Fragmentation')
p.line(x='MSNDATE', y='TONS_IC', line_width=2, source=source, color=Spectral3[2], legend_label='Incendiary')

p.title.text = 'European Theater of Operations'

p.yaxis.axis_label = 'Kilotons of Munitions Dropped'

box_left = pd.to_datetime('6-6-1944')
box_right = pd.to_datetime('16-12-1944')

box = BoxAnnotation(left=box_left, right=box_right,
                    line_width=1, line_color='black', line_dash='dashed',
                    fill_alpha=0.2, fill_color='orange')

p.add_layout(box)

show(p)


# In[104]:


df = pd.read_csv('thor_wwii.csv')

#filter for the European Theater of Operations
filtr = df['THEATER']=='PTO'
df = df[filtr]

df['MSNDATE'] = pd.to_datetime(df['MSNDATE'], format='%m/%d/%Y')
group = df.groupby(pd.Grouper(key='MSNDATE', freq='M'))[['TOTAL_TONS', 'TONS_IC', 'TONS_FRAG']].sum()
group = group / 1000

source = ColumnDataSource(group)

p = figure(x_axis_type="datetime")

p.line(x='MSNDATE', y='TOTAL_TONS', line_width=2, source=source, legend_label='All Munitions')
p.line(x='MSNDATE', y='TONS_FRAG', line_width=2, source=source, color=Spectral3[1], legend_label='Fragmentation')
p.line(x='MSNDATE', y='TONS_IC', line_width=2, source=source, color=Spectral3[2], legend_label='Incendiary')

p.title.text = 'Pacific Theater of Operations'

p.yaxis.axis_label = 'Kilotons of Munitions Dropped'

box_left = pd.to_datetime('19-2-1945')
box_right = pd.to_datetime('15-8-1945')

box = BoxAnnotation(left=box_left, right=box_right,
                    line_width=1, line_color='black', line_dash='dashed',
                    fill_alpha=0.2, fill_color='orange')

p.add_layout(box)

show(p)


# In[12]:


df = pd.read_csv('thor_wwii.csv')
df = df.sample(500)


# In[6]:


def LongLat_to_EN(long, lat):
    try:
        transformer = Transformer.from_crs('epsg:4326', 'epsg:3857')
        easting, northing = transformer.transform(long, lat)
        return easting, northing
    except:
        return None, None


# In[13]:


df['E'], df['N'] = zip(
    *df.apply(lambda x: LongLat_to_EN(x['TGT_LONGITUDE'], x['TGT_LATITUDE']), axis=1))


# In[14]:


grouped = df.groupby(['E', 'N'])[['TONS_IC', 'TONS_FRAG']].sum().reset_index()

filtr = grouped['TONS_FRAG'] != 0
grouped = grouped[filtr]

source = ColumnDataSource(grouped)

left = -2150000
right = 18000000
bottom = -5300000
top = 11000000

p = figure(x_range=Range1d(left, right), y_range=Range1d(bottom, top))


# In[15]:


provider = get_provider('CARTODBPOSITRON')
p.add_tile(provider)

p.circle(x='E', y='N', source=source, line_color='grey', fill_color='yellow')

p.axis.visible = False

show(p)


# In[ ]:


df['N']

