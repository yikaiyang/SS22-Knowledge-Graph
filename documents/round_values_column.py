import pandas as pd
from os import listdir, mkdir
from os.path import isfile, join, isdir

# This script performs following processing tasks on csv files in a specified folder:
# 1) Rounds timestamp to nearest time value (in 20min steps)
# 2) Deduplicates multiple entries by using the first entry

# Folder location 
folderPath = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/traffic/processed'
files = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and not '.DS_Store' in f ]

print(f'Processing files: {files}')
for file in files:
    outputPath = join(folderPath, outputFolder, file)
   
    path = join(folderPath, file)
    print(path)

    df = pd.read_csv(path, delimiter=';')
    df['SpeedUncapped'] = df['SpeedUncapped'].round()
    df['JamFactor'] = df['SpeedUncapped'].round()
    df.to_csv(path, index=False, sep=';')
    print('Processed: '+ path)
