import csv
import json
import os
from pathlib import Path
from tqdm import tqdm
import re
import pandas as pd

from data_linking.util import get_files_for_folder


input_path_folder = 'data/poi/'
output_path_folder = 'data/poi'


def transform_poi():
    working_dir = Path(__file__).parent.parent.parent
    poi_data = []

    files = get_files_for_folder(input_path_folder)
    for file_path in files:
        f = os.path.join(working_dir, file_path)
        # Only processs json
        if f.endswith('.json'):
            file = open(f, 'r')
            file_content = json.load(file)
            results = file_content['results']

            for result in results:
                name = result['name']
                latitude = result['geocodes']['main']['latitude']
                longitude = result['geocodes']['main']['longitude']
                matches = re.findall('([^\/]+)(?=(\.json))', file_path)
                category = matches[0][0]
                if category != None:
                    poi_data.append([category, name, latitude, longitude])
                #if len(matches) > 0:
                #    print(f"{matches[0]}")
            pass
    #print(poi_data)
    resultDF = pd.DataFrame(poi_data, columns=['Category', 'Name', 'CenterLatitude', 'CenterLongitude'])
    resultDF.to_csv(os.path.join(working_dir, output_path_folder, 'poi.csv'), index=False, sep=';')