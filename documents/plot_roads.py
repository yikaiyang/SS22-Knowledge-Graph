import pandas as pd
from os import listdir
from os.path import isfile, join
# import geopandas as gpd
# from geopandas import GeoDataFrame
# import shapely
# import matplotlib.pyplot as plt
import plotly.express as px

# Plots all roads on a map using plotfly

# Folder location 
folderPath = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/traffic/'
files = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and not '.DS_Store' in f ]

resultDF = pd.DataFrame()

print(files)
for file in files:
    path = join(folderPath, file)
    print(path)

    df = pd.read_csv(path, delimiter=';')

    name = df["Street"]
    latitude = df["CenterLatitude"]
    longitude = df["CenterLongitude"]
    df = df.drop_duplicates(subset='Street', keep='first')
    resultDF = resultDF.append(df)
    #df.to_csv(outputPath, index=False, sep=';')
    #print('Processed: '+ outputPath)

print(resultDF)

fig = px.scatter_mapbox(resultDF, lat='CenterLatitude',lon='CenterLongitude', 
    hover_name='Street')
fig.update_layout(mapbox_style="open-street-map")
fig.show() 


# m = Basemap(projection='lcc', resolution=None,
#             width=8E6, height=8E6, 
#             lat_0=45, lon_0=-100,)
# m.etopo(scale=0.5, alpha=0.5)

# # Map (long, lat) to (x, y) for plotting
# x, y = m(-122.3, 47.6)
# plt.plot(x, y, 'ok', markersize=5)
# plt.text(x, y, ' Seattle', fontsize=12);
