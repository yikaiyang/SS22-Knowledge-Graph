import pandas as pd
from os import listdir
import os
from os.path import isfile, join
from tqdm import tqdm
from pathlib import Path

# Lists and exports all roads into a csv file

# Folder location 
folderPath = 'data/traffic/'
outputFile = 'data/roads_list.csv'

working_dir = Path(__file__).parent.parent.parent

input_folder = os.path.join(working_dir, folderPath)
outputFile = os.path.join(working_dir, outputFile)


# This function will create a csv containing a list of all streets
# It does this by traversing through all files in the data/traffic folder and saving their filenames as street name.
def export_all_roads():
    print('Exporting roads to a single csv started.')
    files = [f for f in listdir(input_folder) if isfile(join(input_folder, f)) and not '.DS_Store' in f ]
    resultDF = pd.DataFrame()
    for file in tqdm(files):
        path = join(input_folder, file)

        df = pd.read_csv(path, delimiter=';')
        df = df.drop_duplicates(subset='Street', keep='first')
        resultDF = pd.concat([resultDF, pd.DataFrame(df)], ignore_index=True)
    resultDF.to_csv(outputFile, sep=';', index=False)
    print('Finished: Exporting roads.')