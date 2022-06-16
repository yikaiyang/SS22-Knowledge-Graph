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
    hover_name='Street'
    )
fig.update_layout(mapbox_style="open-street-map")
fig.show() 
