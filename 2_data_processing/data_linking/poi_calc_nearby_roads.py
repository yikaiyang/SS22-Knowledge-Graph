from pathlib import Path
from tqdm import tqdm
import pandas as pd
import os
from haversine import haversine
from .util import get_files_for_folder

NUM_NEAREST_STREETS = 5
POI_FILE_PATH = 'data/poi/poi.csv'
POI_OUTPUT_FILE_PATH = 'data/poi/poi.csv'

def poi_calc_nearby_roads():

    working_dir = Path(__file__).parent.parent.parent
    roadsListFile = os.path.join(working_dir,
                                 'data/roads_list.csv')
    roadsDF = pd.read_csv(roadsListFile, sep=';')
    try: 
        poi_files = get_files_for_folder('data/poi')
        df = pd.read_csv(POI_FILE_PATH, delimiter=';')

        result = []
        for index, row in df.iterrows():
            latitude = row['CenterLatitude']
            longitude = row['CenterLongitude']
            
            #Sort by shortest distance
            roadsDF["Distance"] = roadsDF.apply(lambda road:
                                                    haversine(
                                                        (road['CenterLatitude'], road['CenterLongitude']),
                                                        (latitude, longitude)), axis=1)
            sortedRoadsDF = roadsDF.sort_values("Distance", ascending=True)

            #print(sortedRoadsDF.columns.to_list())
            # Remove roads with distance 0.0 <-> probably same location
            sortedRoadsDF = sortedRoadsDF[sortedRoadsDF['Distance'] > 0.0]

            # nearest_roads = sortedRoadsDF.head(NUM_NEAREST_STREETS)

            # ONLY PICK EVERY 5th ITEM
            nearest_roads = sortedRoadsDF.head(NUM_NEAREST_STREETS * 5)
            nearest_roads = nearest_roads[1::5]

            nearest_streets = []
            for index, road in nearest_roads.iterrows():
                street = road["Street"]
                length = road["Length"]
                streetKey = f"{street}-{length}"
                nearest_streets.append(streetKey)

            nearest_streets_comma_separated = ','.join(nearest_streets)
            result.append(nearest_streets_comma_separated)
        nearest_streets_df = pd.DataFrame(result)
        df['NearestStreets'] = nearest_streets_df
        df.to_csv(POI_OUTPUT_FILE_PATH, sep=';', index=False)
    except Exception as e:
        print(e)
    

    pass