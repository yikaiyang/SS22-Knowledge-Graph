
import http.client, urllib.parse
import requests
import os
from pathlib import Path
import json
import pandas as pd

params = {
    "categories": "",
    "ll": "48.210033,16.363449",
    "limit": 50,
    "radius": 10000,
}

headers = {
    "accept": "application/json",
    "Authorization": "fsq3EQjnWSGr9prH7YF0PSzJLIcqCxMpq07G4upDfxs3EVk="
}

working_dir = Path(__file__).parent.parent

def parse_response(response, out_filename):
    path = os.path.join(working_dir, "data", "poi", f"{str(out_filename)}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    f = open(path, "w")
    f.write(str(json.dumps(response)))
    f.close()
    pass


categories = [
    12057, # Primary School
    12058, # Secondary School
    12059, # High School
    12060, # Middle School
    12061, # Private School
    10058, # Amusement Park
    19030, # Transportation service
    19043, # Bus station
    19047, # Train station
    19046, # Metro Station
    19050, # Tram Station
    19051, # Transportation services
    19054, # Public Transporation
]

 # Crawls top 50 results for each POI sub category (Elementary school, middle school, ...)
 # specified in categories array.
 # See: https://location.foursquare.com/places/docs/categories
 # POIs are located in the viccinity of the geo-coordinates specified in the ll field in the params array.
 # Subsequently the json responses are stored as .json files at 
 # /data/poi/{category}.json for each POI category.
if __name__ == '__main__':

    for category in categories:
        params["categories"] = category 
        host = 'https://api.foursquare.com/v3/places/search'
        response = requests.get(host, params=params, headers=headers)
        print(response.url)
        #print(response.content)
        
        parse_response(response.json(), category)
