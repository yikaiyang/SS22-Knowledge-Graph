from email import header
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from haversine import haversine
from torch import sort

# Given a csv file containing a list featuring latitude and longitude properties it finds nearby roads of a given list (roads_list.csv)
# and creates a 'NearbyStreets' column.

# Folder location 
folderPath = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/roads_list/'
roadsListFile = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/roads_list/roads_list.csv'
outputFile = '../roads_list.csv'

files = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and not '.DS_Store' in f ]
resultDF = pd.DataFrame()
roadsDF = pd.read_csv(roadsListFile, sep=";")

NUM_NEAREST_STREETS = 5

print(files)
for file in files:
    path = join(folderPath, file)
    print(path)

    nearest_streets_df_list = []
    df = pd.read_csv(path, delimiter=';')
    for index, row in df.iterrows():
        latitude = row['CenterLatitude']
        longitude = row['CenterLongitude']

        # Sort by shortest distance
        roadsDF["Distance"] = roadsDF.apply(lambda road: 
            haversine(
                (road['CenterLatitude'], road['CenterLongitude']),
                (latitude, longitude)), axis=1)
        sortedRoadsDF = roadsDF.sort_values("Distance", ascending=True)

        print(sortedRoadsDF.columns.to_list())
        #Remove roads with distance 0.0 <-> probably same location
        sortedRoadsDF = sortedRoadsDF[sortedRoadsDF['Distance'] > 0.0]

        #nearest_roads = sortedRoadsDF.head(NUM_NEAREST_STREETS)
        
        # ONLY PICK EVERY 5th ITEM
        nearest_roads = sortedRoadsDF.head(NUM_NEAREST_STREETS*5)
        nearest_roads = nearest_roads[1::5]
    
        nearest_streets = []
        for index, road in nearest_roads.iterrows():
            street = road["Street"]
            length = road["Length"]
            streetKey = f"{street}-{length}"
            nearest_streets.append(streetKey)
        
        nearest_streets_comma_separated = ','.join(nearest_streets)
        nearest_streets_df_list.append(nearest_streets_comma_separated)
        
        print(f"Processed row: {row}")
        #print(f"Nearest streets for {row['Description']}: {nearest_five_roads}")
    nearest_streets_df = pd.DataFrame(nearest_streets_df_list)
    df['NearestStreets'] = nearest_streets_df

    print(df)
    df.to_csv(path, sep=';', index=False)