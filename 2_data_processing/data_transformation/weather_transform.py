import csv
import json
import os
from pathlib import Path
from tqdm import tqdm

input_path = 'data/raw/weather_data.csv'
output_path = 'data/weather'

def _remove_previous_files():
    working_dir = Path(__file__).parent.parent.parent
    file_path = os.path.join(working_dir, output_path, ''.join(["weather", ".csv"]))
    file_exists = os.path.exists(file_path)

    # Delete existing file
    if file_exists:
        os.remove(file_path)
        print('Previous transformed file detected. Overwriting existing file.')

def transform_weather() -> None:
    working_dir = Path(__file__).parent.parent.parent
    file = os.path.join(working_dir, input_path)
    # Output folder
    directory_path = os.path.join(working_dir, output_path)
    print(f'Reading file from: {file}')

    _remove_previous_files()

    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        header = next(reader)
        for index, row in enumerate(tqdm(reader)):
            # for column in row:
            time = row[0]
            del row[0]
            jsonString = ",".join([str(i) for i in row])
            jsonString = jsonString.replace("\"\"", "\"")
            jsonString = jsonString[1:-1]

            # print(jsonString)
            # Iterate through each location
            jsonObject = json.loads(jsonString)
            # Iterate through each location
          
            try:
                centerLatitude = jsonObject['coord']['lat']
                centerLongitude = jsonObject['coord']['lon']
                weather = jsonObject['weather'][0]['main']
                temp = jsonObject['main']['temp']
                timestamp = time

                file_path = os.path.join(directory_path, ''.join(["weather.csv"]))
                file_existed = os.path.exists(file_path)

                # Write to file
                with (open(file_path, 'a')) as outFileLocation:
                    csvwriter = csv.writer(outFileLocation, delimiter=';')
                    if not file_existed:
                        # File was just created
                        csvwriter.writerow([
                            "Timestamp",
                            "Weather",
                            "Temp",
                            "CenterLatitude",
                            "CenterLongitude",
                        ])

                    csvwriter.writerow([
                        timestamp,
                        weather,
                        temp,
                        centerLatitude,
                        centerLongitude,
                    ])
                    outFileLocation.close()
            except UnicodeEncodeError as err:
                    print(err)
            except Exception as inst:
                    print(type(inst))
    print(f'Transformation complete: {file}')
