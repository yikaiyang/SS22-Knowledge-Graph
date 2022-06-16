import csv
import json
import os

file = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/crawled_unprocessed_data/incidents.csv'
with open(file) as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    header = next(reader)
    for index, row in enumerate(reader):
        #for column in row:
        time = row[0]
        jsonString = row[1]
       
        directory_path = os.getcwd() + '/documents/data/incidents/'
       
        jsonString = jsonString.replace("\"\"", "\"")
        jsonString = jsonString[1:-1]
        jsonObject = json.loads(jsonString)
        results = jsonObject["results"]
        #Iterate through each location
        for arrayObject in jsonObject["results"]:
            try:
                timestamp = time
                #print(timestamp)
                #print(arrayObject)
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
                    
                file_path = os.path.join(directory_path, ''.join(["incidents", ".csv"]))
                file_existed = os.path.exists(file_path)

                # #File
                with (open(file_path, 'a')) as outFileLocation:
                    csvwriter = csv.writer(outFileLocation, delimiter=';')
                    if not file_existed:
                        #File was just created
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
                    #outFileLocation.write(description)
                    outFileLocation.close()
            except Exception as inst:
                print(type(inst))