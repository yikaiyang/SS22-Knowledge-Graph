from logging import critical
from unicodedata import name
from neo4j import GraphDatabase
import pandas as pd
import os
from dateutil import parser

class Neo4JIntegration:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def createEntities(self):
        self.loadIncidents()
        self.loadRoads()
        self.loadWeather()

    def loadIncidents(self):
        folderPath = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/incidents/processed'
        files = Neo4JIntegration._getFilesOfDir(folderPath)
        for file in files:
            filePath = os.path.join(folderPath,file)
            print(filePath)
            incidentsDF = pd.read_csv(filePath, delimiter=';')
            print(incidentsDF.columns.tolist())
            for index, incident in incidentsDF.iterrows():
                print(incident["IncidentType"])
                with self.driver.session() as session:
                    session.write_transaction(self._create_incident, incident)
    

    @staticmethod
    def _create_incident(tx, incident):
        print(f"Creating incident {incident['IncidentType']} criticality: {incident['Criticality']}")
        incidentType = incident["IncidentType"]
        criticality = incident["Criticality"]
        timestamp = incident["Timestamp"]
        time = parser.parse(timestamp)
        hour = time.hour
        minute = time.minute
        stmt = f"""
            MERGE (i:Incident
                {{
                    name: '{incidentType}',
                    incidentType: '{incidentType}',
                    criticality: '{criticality}' 
                }}
            )<-[:HAS_INCIDENT]-(
                t:Time
                {{
                    hour: {hour},
                    minute: {minute}
                }}
            )
            RETURN i;
        """
        result = tx.run(stmt)
        return result

    ### Create Roads
    def loadRoads(self):
        folderPath = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/traffic/processed'
        files = Neo4JIntegration._getFilesOfDir(folderPath)
        for file in files:
            filePath = os.path.join(folderPath,file)
            print(filePath)
            roadsDF = pd.read_csv(filePath, delimiter=';', encoding="utf-8")
            print(roadsDF.columns.tolist())
            roadsDF = roadsDF.drop_duplicates(subset=['Street', 'Length', 'CenterLatitude', 'CenterLongitude'])
           
            for index, road in roadsDF.iterrows():
                print(road["Street"])
                with self.driver.session() as session:
                    session.write_transaction(self._create_road, road)


    @staticmethod
    def _create_road(tx, road):
        print(f"Creating road {road['Street']}")
        streetName = road["Street"]
        length = road["Length"]
        name = streetName
        latitude = road["CenterLatitude"]
        longitude = road["CenterLongitude"]
 
        stmt = f"""
            MERGE (r:Road
                {{
                    name: '{name}-{length}',
                    length: '{length}',
                    latitude: {latitude},
                    longitude: {longitude}
                }}
            )
            RETURN r;"""
        result = tx.run(stmt)
        return result

    
    ### Create weather
    def loadWeather(self):
        folderPath = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/weather/processed'
        files = Neo4JIntegration._getFilesOfDir(folderPath)
        for file in files:
            filePath = os.path.join(folderPath,file)
            print(filePath)
            weatherDF = pd.read_csv(filePath, delimiter=';')
            print(weatherDF.columns.tolist())
            for index, weather in weatherDF.iterrows():
                print(weather["Temp"])
                with self.driver.session() as session:
                    session.write_transaction(self._create_weather, weather)

    @staticmethod
    def _create_weather(tx, weatherObject):
        print(f"Creating weather: {weatherObject['Weather']}")
        weather = weatherObject["Weather"]
        latitude = weatherObject["Latitude"]
        longitude = weatherObject["Longitude"]
        temp = weatherObject["Temp"]
         
        # temp: {temp},
        # latitude: '{latitude}',
        # longitude: '{longitude}',
        stmt = f"""
            MERGE (w:Weather
                {{
                    name: '{weather}'
                }}
            )
            RETURN w;
        """
        result = tx.run(stmt)
        return result

    #def createRelationships(self):

    @staticmethod
    def _getFilesOfDir(dir_path):
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and not f == '.DS_Store']
        return files


if __name__ == "__main__":
    connection = Neo4JIntegration("bolt://localhost:7687", "neo4j", "")
    connection.createEntities()
    connection.close()