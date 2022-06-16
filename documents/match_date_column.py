import pandas as pd
from os import listdir, mkdir
from os.path import isfile, join, isdir
import re
# This script performs following processing tasks on csv files in a specified folder:
# 1) Rounds timestamp to nearest time value (in 20min steps)
# 2) Deduplicates multiple entries by using the first entry

# Folder location 
folderPath = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/incidents'
files = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and not '.DS_Store' in f ]

print(files)
outputFolder = 'processed'
outputDirPath = join(folderPath, outputFolder)

# Create output folder if it does not exist
if not isdir(outputDirPath):
    mkdir(outputDirPath)

for file in files:
    outputPath = join(folderPath, outputFolder, file)
   
    path = join(folderPath, file)
    print(path)

    df = pd.read_csv(path, delimiter=';')
    pdts = pd.to_datetime(df["Timestamp"])
    rounded_pdts = pdts.map(lambda x: x.round(freq='20T'))
    df["Timestamp"] = rounded_pdts
    df = df.drop_duplicates(subset='Timestamp', keep='first')
    #print(df)
    df.to_csv(outputPath, index=False, sep=';')
    print('Processed: '+ outputPath)
