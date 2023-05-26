import csv
import json
import os
from pathlib import Path
from tqdm import tqdm

input_path = 'data/raw/incidents.csv'
output_path = 'data/incidents'

def _remove_previous_files():
    working_dir = Path(__file__).parent.parent.parent
    file_path = os.path.join(working_dir, output_path, ''.join(["incidents", ".csv"]))
    file_exists = os.path.exists(file_path)
    
    # Delete existing file
    if file_exists:
        os.remove(file_path)
        print('Previous transformed file detected. Overwriting existing file.')

def transform_incidents() -> None:
    working_dir = Path(__file__).parent.parent.parent
    file = os.path.join(working_dir, input_path)
    
    _remove_previous_files()

    print(f'Reading file from: {file}')

    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        header = next(reader)
        for index, row in enumerate(tqdm(reader)):
            # for column in row:
            time = row[0]
            jsonString = row[1]

            jsonString = jsonString.replace("\"\"", "\"")
            jsonString = jsonString[1:-1]
            jsonObject = json.loads(jsonString)
            results = jsonObject["results"]
            # Iterate through each location
            for arrayObject in jsonObject["results"]:
                try:
                    timestamp = time
                    type = arrayObject["incidentDetails"]["type"]
                    description = arrayObject["incidentDetails"]["description"]["value"]
                    criticality = arrayObject["incidentDetails"]["criticality"]
                    shape = arrayObject["location"]["shape"]
                    roadClosed = arrayObject["incidentDetails"]["roadClosed"]
                    startTime = arrayObject["incidentDetails"]["startTime"]
                    endTime = arrayObject["incidentDetails"]["endTime"]
                    entryTime = arrayObject["incidentDetails"]["entryTime"]
                    # Calculate center latitude / center longitude
                    links = arrayObject["location"]["shape"]["links"]
                    id = arrayObject["incidentDetails"]["id"]
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
                            
                    # Write transformed file
                    working_dir = Path(__file__).parent.parent.parent
                    file_path = os.path.join(working_dir, output_path, ''.join(["incidents", ".csv"]))
                    file_exists = os.path.exists(file_path)
                    

                    # #File
                    with (open(file_path, 'a')) as outFileLocation:
                        csvwriter = csv.writer(outFileLocation, delimiter=';')
                        if not file_exists:
                            # File was just created
                            csvwriter.writerow([
                                "Timestamp",
                                "ID",
                                "IncidentType",
                                "Description",
                                "Criticality",
                                "Shape",
                                "RoadClosed",
                                "StartTime",
                                "EndTime",
                                "EntryTime",
                                "CenterLatitude",
                                "CenterLongitude"
                            ])

                        csvwriter.writerow([
                            timestamp,
                            id,
                            type,
                            description,
                            criticality,
                            shape,
                            roadClosed,
                            startTime,
                            endTime,
                            entryTime,
                            centerLatitude,
                            centerLongitude,
                        ])
                        # outFileLocation.write(description)
                        outFileLocation.close()
                except Exception as e:
                    print(e)
        print("Transformation 'incidents' completed")
                
