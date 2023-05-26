import csv
import json
import os
from pathlib import Path
from tqdm import tqdm

input_path = 'data/raw/traffic.csv'
output_path = 'data/traffic'

def transform_traffic():
    working_dir = Path(__file__).parent.parent.parent
    file = os.path.join(working_dir, input_path)
    print(f'Reading file from: {file}')
    # Output folder
    directory_path = os.path.join(working_dir, output_path)


    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        header = next(reader)
        for index, row in enumerate(tqdm(reader)):
            #for column in row:
            time = row[0]
            del row[0]
           
            jsonString = ",".join([str(i) for i in row])
            jsonString = jsonString.replace("\"\"", "\"")
            jsonString = jsonString[1:-1]
    
            jsonObject = json.loads(jsonString)
            #Iterate through each location
            for arrayObject in jsonObject:
                try:
                    description = arrayObject["location"]["description"]
    
                    # Calculate center latitude / center longitude
                    links = arrayObject["location"]["shape"]["links"]
                    centerLatitude = 0
                    centerLongitude = 0
                    for linkIdx, link in enumerate(links):
                        points = link["points"]
                        for point in points:
                            centerLatitude += point["lat"]
                            centerLongitude += point["lng"]
                        
                        if linkIdx == 0 and linkIdx == 0:
                            centerLatitude /= (len(points))
                            centerLongitude /= (len(points))
                        else:
                            centerLatitude /= (len(points) + 1)
                            centerLongitude /= (len(points) + 1)
    
                    length = arrayObject["location"]["length"]
                    shape = json.dumps(arrayObject["location"]["shape"])
                    speed = arrayObject["currentFlow"]["speed"]
                    speedUncapped = arrayObject["currentFlow"]["speedUncapped"]
                    freeFlow = arrayObject["currentFlow"]["freeFlow"]
                    jamFactor = arrayObject["currentFlow"]["jamFactor"]
                    confidence = arrayObject["currentFlow"]["confidence"]
                    traversibility = arrayObject["currentFlow"]["traversability"]
                    timestamp = time
                  
                    #print(description)
    
                    file_path = os.path.join(directory_path, ''.join([description, "-", str(length), ".csv"]))
                    file_existed = os.path.exists(file_path)
    
                    #print(file_path)
                    # Write to file
                    with (open(file_path, 'a')) as outFileLocation:
                        csvwriter = csv.writer(outFileLocation, delimiter=';')
                        if not file_existed:
                            #File was just created
                            csvwriter.writerow([
                                "Timestamp",
                                "Street", 
                                "CenterLatitude", 
                                "CenterLongitude", 
                                "Length", 
                                "Shape",
                                "Speed", 
                                "SpeedUncapped", 
                                "FreeFlow", 
                                "JamFactor", 
                                "Confidence", 
                                "Traversibility"
                            ])
    
                        csvwriter.writerow([
                            timestamp,
                            description,
                            centerLatitude,
                            centerLongitude,
                            length,
                            shape,
                            speed,
                            speedUncapped,
                            freeFlow,
                            jamFactor,
                            confidence, 
                            traversibility
                        ])
                        #outFileLocation.write(description)
                        outFileLocation.close()
                except UnicodeEncodeError as err:
                    pass
                    #print(err)
                except Exception as inst:
                    pass
                    #print(type(inst))
    