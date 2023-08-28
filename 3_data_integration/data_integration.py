from neo4j import GraphDatabase
import pandas as pd
import os
from dateutil import parser
from datetime import datetime, timedelta
from pathlib import Path
from tqdm import tqdm

working_dir = Path(__file__).parent.parent

class Neo4JIntegration:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def delete_db(self):
        self.driver.execute_query(
            """
             MATCH (n)
             DETACH DELETE n
            """
        )

    def createEntities(self):
        self.loadIncidents()
        self.loadRoads()
        self.loadDateAndTime()
        self.loadWeather()
        self.load_poi()

    #region Create incidents
    def loadIncidents(self):
        folderPath = os.path.join(working_dir, 'data/incidents')
        files = Neo4JIntegration._getFilesOfDir(folderPath)
        for file in files:
            filePath = os.path.join(folderPath,file)
            incidentsDF = pd.read_csv(filePath, delimiter=';')
            for index, incident in tqdm(incidentsDF.iterrows()):
                #t.set_description(f"Processing incident: {incident['IncidentType']}")
                with self.driver.session() as session:
                    session.write_transaction(self._create_incident, incident)
    

    @staticmethod
    def _create_incident(tx, incident):
        #print(f"Creating incident {incident['IncidentType']} criticality: {incident['Criticality']}")
        incidentType = incident["IncidentType"]
        criticality = incident["Criticality"]
        latitude = incident["CenterLatitude"]
        longitude = incident["CenterLongitude"]
        timestamp = incident["Timestamp"]
        time = parser.parse(timestamp)
        hour = time.hour
        minute = time.minute
        day = time.day
        month = time.month
        year = time.year

        stmt = f"""
            MERGE (d: DateTime
                {{
                    name: '{day}-{month}-{year} {hour}:{minute}',
                    hour: {hour},
                    minute: {minute},
                    day: {day},
                    month: {month},
                    year: {year}
                }}
            )
            MERGE (i:Incident
                {{
                    name: '{incidentType}',
                    incidentType: '{incidentType}',
                    criticality: '{criticality}',
                    latitude: '{latitude}',
                    longitude: '{longitude}'
                }}
            )
            MERGE (i)<-[:HAS_INCIDENT]-(d)
            RETURN i;
        """
        result = tx.run(stmt)
        return result
    #endregion

    #region Create roads
    def loadRoads(self):
        folderPath = os.path.join(working_dir, 'data/traffic')
        files = Neo4JIntegration._getFilesOfDir(folderPath)
        for file in (t := tqdm(files)):
            filePath = os.path.join(folderPath,file)
            t.set_description(f"Creating DB entry for: {filePath}")

            roadsDF = pd.read_csv(filePath, delimiter=';', encoding="utf-8")
            roadsDF = roadsDF.drop_duplicates(subset=['Street', 'Length', 'CenterLatitude', 'CenterLongitude'])
           
            for index, road in roadsDF.iterrows():
                with self.driver.session() as session:
                    session.write_transaction(self._create_road, road)


    @staticmethod
    def _create_road(tx, road):
        #print(f"Creating road {road['Street']}")
        streetName = road["Street"]
        length = road["Length"]
        name = f"{streetName}-{length}"
        latitude = road["CenterLatitude"]
        longitude = road["CenterLongitude"]
        timestamp = road["Timestamp"]
        time = parser.parse(timestamp)

        stmt = f"""
            MERGE (r:Road
                {{
                    name: '{name}',
                    length: '{length}',
                    latitude: {latitude},
                    longitude: {longitude}
                }}
            )
            RETURN r;"""
        result = tx.run(stmt)
        return result
    #endregion
    
    #region Create weather
    def loadWeather(self):
        folderPath = os.path.join(working_dir, 'data/weather')
        files = Neo4JIntegration._getFilesOfDir(folderPath)
        for file in files:
            filePath = os.path.join(folderPath,file)
            weatherDF = pd.read_csv(filePath, delimiter=';')
            for index, weather in (t := tqdm(weatherDF.iterrows())):
                t.set_description(f"Processing {weather['Temp']}")
                with self.driver.session() as session:
                    session.write_transaction(self._create_weather, weather)

    @staticmethod
    def _create_weather(tx, weatherObject):
        #print(f"Creating weather: {weatherObject['Weather']}")
        weather = weatherObject["Weather"]
        latitude = weatherObject["CenterLatitude"]
        longitude = weatherObject["CenterLongitude"]
        temp = weatherObject["Temp"]
        timestamp = weatherObject["Timestamp"]
        time = parser.parse(timestamp)
        hour = time.hour
        minute = time.minute
        day = time.day
        month = time.month
        year = time.year

        stmt = f"""
            MERGE (d: DateTime
                {{
                    name: '{day}-{month}-{year} {hour}:{minute}',
                    hour: {hour},
                    minute: {minute},
                    day: {day},
                    month: {month},
                    year: {year}
                }}
            )

            MERGE (w:Weather
                {{
                    name: '{weather}'
                }}
            )<-[:HAS_WEATHER]-(d)

            MERGE (t:Temperature
                {{
                    name: '{temp}'
                }}
            )<-[:HAS_TEMPERATURE]-(d)
            RETURN w,t;
        """
        result = tx.run(stmt)
        return result
    #endregion
    
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
        #print(f"Creating date and time: {date}")
        
        hour = date.hour
        minute = date.minute
        day = date.day
        month = date.month
        year = date.year

        stmt = f"""
            MERGE (d: DateTime
                {{
                    name: '{day}-{month}-{year} {hour}:{minute}',
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
        self.load_road_network()
        self.load_road_traffic_situation()

    def load_incident_rel(self):
        folderPath = os.path.join(working_dir, 'data/incidents')
        files = Neo4JIntegration._getFilesOfDir(folderPath)
        for file in files:
            filePath = os.path.join(folderPath,file)
            #print(filePath)
            incidentsDF = pd.read_csv(filePath, delimiter=';')
            #print(incidentsDF.columns.tolist())
            for index, incident in tqdm(incidentsDF.iterrows()):
                #print(incident["IncidentType"])
                with self.driver.session() as session:
                    session.write_transaction(self._create_incident_relationship, incident)
    
    @staticmethod
    def _create_incident_relationship(tx, incident):
        #print(f"Creating relationships for incident: {incident['IncidentType']}")
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
            MERGE (i)-[:IS_NEARBY]->(r{i})
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
            MERGE (d: DateTime
                {{
                    name: '{day}-{month}-{year} {hour}:{minute}',
                    hour: {hour},
                    minute: {minute},
                    day: {day},
                    month: {month},
                    year: {year}
                }}
            )
            MERGE (i)<-[:HAS_INCIDENT]-(d)
            {merge_clauses_incident_street_stmt}
            RETURN i;
        """
        #print(stmt)
        result = tx.run(stmt)
        return result


    #region Road Network
    #### Road relationship (r:Road)-[:IS_CONNECTED]->(r2:Road)
    def load_road_network(self):
        filePath = os.path.join(working_dir, 'data/roads_list.csv')
        roadsDF = pd.read_csv(filePath, delimiter=';')
        for index, road in tqdm(roadsDF.iterrows()):
            with self.driver.session() as session:
                session.write_transaction(self._create_road_network_relationship, road)

    @staticmethod
    def _create_road_network_relationship(tx, road):
        #print(f"Creating nearby roads for: {road}")
        name = road["Street"]
        length = road["Length"]
        road_key = f"{name}-{length}"
        try:
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
            #print(stmt)
            result = tx.run(stmt)
            return result
        except:
            return None
    #endregion

    
    #region Create road traffic situation relationships
    def load_road_traffic_situation(self):
        folderPath = os.path.join(working_dir, 'data/traffic')
        files = Neo4JIntegration._getFilesOfDir(folderPath)
        for file in (t:=tqdm(files)):
            t.set_description(f"Creating relationship: Traffic situation: {file}")

            filePath = os.path.join(folderPath,file)
            #print(filePath)
            roadsDF = pd.read_csv(filePath, delimiter=';')
            for index, road in roadsDF.iterrows():
                with self.driver.session() as session:
                    session.write_transaction(self._create_road_traffic_situation_rel, road)

    @staticmethod
    def _create_road_traffic_situation_rel(tx, road):
        #print(f"Creating road <-> traffic situation relationship: {road}")
        name = road["Street"]
        length = road["Length"]
        road_key = f"{name}-{length}"
        
        speedUncapped = road["Speed"]
        jamFactor = road["JamFactor"]
        timestamp = road["Timestamp"]
        time = parser.parse(timestamp)
        hour = time.hour
        minute = time.minute
        day = time.day
        month = time.month
        year = time.year

        stmt = f"""
            MATCH (r:Road {{ name: '{road_key}'}})
            MERGE (t: TrafficSituation {{ speed: {speedUncapped}}})
            MERGE (d: DateTime
                {{
                    name: '{day}-{month}-{year} {hour}:{minute}',
                    hour: {hour},
                    minute: {minute},
                    day: {day},
                    month: {month},
                    year: {year}
                }}
            )
            MERGE (t)<-[:HAS_TRAFFIC_SITUATION]-(d)
            RETURN r;
        """
        #print(stmt)
        result = tx.run(stmt)
        return result
    #endregion

    def load_poi(self):
        ## TODO LOAD Poi
        POI_FILE_PATH = 'data/poi/poi.csv'
        filePath = os.path.join(working_dir,POI_FILE_PATH)
        #print(filePath)
        df = pd.read_csv(filePath, delimiter=';')
        for index, item in (t:=tqdm(df.iterrows())):
            t.set_description(f"Creating POI: {item['Name']}")
            with self.driver.session() as session:
                session.write_transaction(self._create_poi, item)

    @staticmethod
    def _create_poi(tx, poi):
        name = poi['Name']
        latitude = poi['CenterLatitude']
        longitude = poi['CenterLongitude']
        category = poi['Category']

        try:
            nearbyStreetsString = poi["NearestStreets"] 
            nearbyStreets = (nearbyStreetsString).split(',')
    
            match_clauses = [f"(r{i}:Road {{ name: '{x}'}})" for i,x in enumerate(nearbyStreets)]
            match_clauses_stmt = ','.join(match_clauses)

            merge_clauses_road_street = [f"""
                MERGE (p)-[:IS_LOCATED]->(r{i})
            """ for i,x in enumerate(nearbyStreets)]

            merge_clauses_roads_stmt = ''.join(merge_clauses_road_street)

            stmt = f"""
                MATCH {
                    match_clauses_stmt
                }
                MERGE (p: POI 
                    {{ 
                        name: '{name}',
                        latitude: {latitude},
                        longitude: {longitude},
                        category: '{category}'
                    }}
                )
                {merge_clauses_roads_stmt}
                RETURN p;
            """
            #print(stmt)
            result = tx.run(stmt)
            return result
        except:
            return None
        

    @staticmethod
    def _getFilesOfDir(dir_path):
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and not f == '.DS_Store']
        return files