from neo4j import GraphDatabase
import pandas as pd
import os
from dateutil import parser
from datetime import datetime, timedelta

class Neo4JIntegration:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def createEntities(self):
        self.loadIncidents()
        self.loadRoads()
        self.loadDateAndTime()
        self.loadWeather()

    def loadIncidents(self):
        folderPath = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/incidents/processed'
        files = Neo4JIntegration._getFilesOfDir(folderPath)
        for file in files:
            filePath = os.path.join(folderPath,file)
            print(filePath)
            incidentsDF = pd.read_csv(filePath, delimiter=';')
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
        day = time.day
        month = time.month
        year = time.year

        stmt = f"""
            MERGE (i:Incident
                {{
                    name: '{incidentType}',
                    incidentType: '{incidentType}',
                    criticality: '{criticality}' 
                }}
            )<-[:HAS_INCIDENT]-(d: DateTime
                {{
                    hour: {hour},
                    minute: {minute},
                    day: {day},
                    month: {month},
                    year: {year}
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
        timestamp = weatherObject["Timestamp"]
        time = parser.parse(timestamp)
        hour = time.hour
        minute = time.minute
        day = time.day
        month = time.month
        year = time.year

        stmt = f"""
            MERGE (w:Weather
                {{
                    name: '{weather}'
                }}
            )<-[:HAS_WEATHER]-(d: DateTime
                {{
                    hour: {hour},
                    minute: {minute},
                    day: {day},
                    month: {month},
                    year: {year}
                }}
            )

            MERGE (t:Temperature
                {{
                    name: '{temp}'
                }}
            )<-[:HAS_TEMPERATURE]-(d2: DateTime
                {{
                    hour: {hour},
                    minute: {minute},
                    day: {day},
                    month: {month},
                    year: {year}
                }}
            )
            RETURN w,t;
        """
        result = tx.run(stmt)
        return result
    
     ### Create date and time nodes
    def loadDateAndTime(self):
        with self.driver.session() as session:
            # 2022-05-10 14:40:00
            start_time = datetime(2022,5,10,14,00)
            end_time = datetime(2022,5,18,14,00)
            delta = timedelta(minutes=20)
            while start_time < end_time:
                session.write_transaction(self._create_date_and_time, start_time)
                start_time += delta
            #session.write_transaction(self._create_date_and_time, weather)

    @staticmethod
    def _create_date_and_time(tx, date):
        print(f"Creating date and time: {date}")
        
        hour = date.hour
        minute = date.minute
        day = date.day
        month = date.month
        year = date.year

        stmt = f"""
            MERGE (d: DateTime
                {{
                    hour: {hour},
                    minute: {minute},
                    day: {day},
                    month: {month},
                    year: {year}
                }}
            )
            RETURN d
        """
        result = tx.run(stmt)
        return result


    def createRelationships(self):
        self.load_incident_rel()
        self.load_road_rel()

    def load_incident_rel(self):
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
                    session.write_transaction(self._create_incident_relationship, incident)
    
    @staticmethod
    def _create_incident_relationship(tx, incident):
        print(f"Creating incident {incident['IncidentType']} criticality: {incident['Criticality']}")
        incidentType = incident["IncidentType"]
        criticality = incident["Criticality"]
        timestamp = incident["Timestamp"]
        nearbyStreetsString = incident["NearestStreets"]
        nearbyStreets = (nearbyStreetsString).split(',')
        time = parser.parse(timestamp)
        hour = time.hour
        minute = time.minute
        day = time.day
        month = time.month
        year = time.year

        match_clauses = [f"(r{i}:Road {{ name: '{x}'}})" for i,x in enumerate(nearbyStreets)]
        match_clauses_stmt = ','.join(match_clauses)

        merge_clauses_incident_street = [f"""
            MERGE (i)<-[:IS_NEARBY]-(r{i})
        """ for i,x in enumerate(nearbyStreets)]

        merge_clauses_incident_street_stmt = ''.join(merge_clauses_incident_street)

        stmt = f"""
            MATCH {
                match_clauses_stmt
            }
            MERGE (i:Incident
                {{
                    name: '{incidentType}',
                    incidentType: '{incidentType}',
                    criticality: '{criticality}' 
                }})

            MERGE (i)<-[:HAS_INCIDENT]-(d: DateTime
                {{
                    name: '{day}-{month}-{year} {hour}:{minute}',
                    hour: {hour},
                    minute: {minute},
                    day: {day},
                    month: {month},
                    year: {year}
                }}
            )
            {merge_clauses_incident_street_stmt}
            RETURN i;
        """
        print(stmt)
        result = tx.run(stmt)
        return result

    #### Road relationship (r:Road)-[:IS_CONNECTED]->(r2:Road)
    def load_road_rel(self):
        filePath = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/documents/data/roads_list/roads_list.csv'
        roadsDF = pd.read_csv(filePath, delimiter=';')
        for index, road in roadsDF.iterrows():
            with self.driver.session() as session:
                session.write_transaction(self._create_road_relationship, road)

    @staticmethod
    def _create_road_relationship(tx, road):
        print(f"Creating road {road}")
        name = road["Street"]
        length = road["Length"]
        road_key = f"{name}-{length}"
        nearbyStreetsString = road["NearestStreets"]
        nearbyStreets = (nearbyStreetsString).split(',')

        match_clauses = [f"(r{i}:Road {{ name: '{x}'}})" for i,x in enumerate(nearbyStreets)]
        match_clauses.append(f"(r:Road {{ name: '{road_key}'}})" )
        match_clauses_stmt = ','.join(match_clauses)

        merge_clauses_road_street = [f"""
            MERGE (r)<-[:IS_CONNECTED]-(r{i})
        """ for i,x in enumerate(nearbyStreets)]

        merge_clauses_roads_stmt = ''.join(merge_clauses_road_street)

        stmt = f"""
            MATCH {
                match_clauses_stmt
            }
            {merge_clauses_roads_stmt}
            RETURN r;
        """
        print(stmt)
        result = tx.run(stmt)
        return result
        
    def _create_road_traffic_situation_rel(tx, road):
        print(f"Creating road <-> traffic situation relationship: {road}")
        name = road["Street"]
        length = road["Length"]
        road_key = f"{name}-{length}"
        
        match_clauses = []
        match_clauses.append(f"(r:Road {{ name: '{road_key}'}})" )
        
        #merge_clauses_road_street = [f"""
        #    MERGE (r)<-[:IS_CONNECTED]-(r{i})
        #""" for i,x in enumerate(nearbyStreets)]


    @staticmethod
    def _getFilesOfDir(dir_path):
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and not f == '.DS_Store']
        return files


if __name__ == "__main__":
    connection = Neo4JIntegration("bolt://localhost:7687", "neo4j", "kgtransport")
    connection.createEntities()
    connection.createRelationships()
    connection.close()