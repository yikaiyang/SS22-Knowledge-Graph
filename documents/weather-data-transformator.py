import csv
import json
import os

file = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/crawled_unprocessed_data/weather_data.csv'
with open(file) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    header = next(reader)
    for index, row in enumerate(reader):
        #for column in row:
        time = row[0]
        del row[0]
        directory_path = os.getcwd() + '/documents/data/weather/'

        jsonString = ",".join([str(i) for i in row])
        jsonString = jsonString.replace("\"\"", "\"")
        jsonString = jsonString[1:-1]

        #print(jsonString)

        jsonObject = json.loads(jsonString)
        #print(jsonObject)
        #Iterate through each location
        jsonObject = json.loads(jsonString)
        #Iterate through each location
        for arrayObject in jsonObject:
            try:
                description = arrayObject["location"]["description"]

                # Calculate center latitude / center longitude
                links = arrayObject["location"]["shape"]["links"]
                centerLatitude = 0
                centerLongitude = 0
                for link in links:
                    points = link["points"]
                    for point in points:
                        centerLatitude += point["lat"]
                        centerLongitude += point["lng"]
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
              
                print(description)

                file_path = os.path.join(directory_path, ''.join([description, "-", str(length), ".csv"]))
                file_existed = os.path.exists(file_path)

                print(file_path)
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
                print(err)
            except Exception as inst:
                print(type(inst))