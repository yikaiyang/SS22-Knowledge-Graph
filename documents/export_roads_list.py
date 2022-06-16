import pandas as pd
from os import listdir
from os.path import isfile, join

import plotly.express as px

# Lists and exports all roads into a csv file

# Folder location 
folderPath = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/traffic/'
outputFile = '../roads_list/roads_list.csv'

files = [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and not '.DS_Store' in f ]
resultDF = pd.DataFrame()
print(files)
for file in files:
    path = join(folderPath, file)
    print(path)

    df = pd.read_csv(path, delimiter=';')
    df = df.drop_duplicates(subset='Street', keep='first')
    resultDF = resultDF.append(df)

print(resultDF)
resultDF.to_csv(join(folderPath, outputFile), sep=';', index=False)