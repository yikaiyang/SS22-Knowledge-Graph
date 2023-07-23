import pandas as pd
from os import listdir, mkdir
from os.path import isfile, join, isdir
from pathlib import Path
import os
from tqdm import tqdm

import re
# This script performs following processing tasks on csv files in a specified folder:
# 1) Rounds timestamp to nearest time value (in 20min steps)
# 2) Deduplicates multiple entries by using the first entry

# Folder location 
folderPaths = ['data/traffic']

def match_speed():
    for folderPath in folderPaths:
        working_dir = Path(__file__).parent.parent.parent
        folderPath = os.path.join(working_dir, folderPath)
        files = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and not '.DS_Store' in f]
        # outputFolder = 'processed'
        # outputDirPath = join(folderPath, outputFolder)
        # 
        # # Create output folder if it does not exist
        # if not isdir(outputDirPath):
        #     mkdir(outputDirPath)

        for file in (t := tqdm(files)):
            outputPath = join(folderPath, file)
            path = join(folderPath, file)

            df = pd.read_csv(path, delimiter=';')
            pdts = df["Speed"]
            rounded_pdts = pdts.map(lambda x: round(x))
            df["Speed"] = rounded_pdts
            #df = df.drop_duplicates(subset='Timestamp', keep='first')
            df.to_csv(f'{outputPath}', index=False, sep=';')

            t.set_description(f"Processing: {outputPath}")
