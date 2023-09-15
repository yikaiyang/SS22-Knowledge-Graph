from rest_framework.views import APIView
from rest_framework.response import Response
from models.poi import POI
from models.road import Road
from models.incident import Incident
from models.date import Date
from models.time import Time
from models.temperature import Temperature
from models.traffic_situation import TrafficSituation
from models.weather import Weather
import neomodel

from .predict import predict_tail

# MATCH r=((p:POI{name:'Bundesrealgymnasium Albertgasse'})-[:IS_LOCATED]-()) RETURN r


class GetPredictedRelatedNodes(APIView):
    def get(self, request):
        result = {
            'node_id': request.GET.get('id', 'NodeID'),
            'name': request.GET.get('name'),
            'prediction_model': request.GET.get('p'),
            'relationship': request.GET.get('r', '')
        }

        id = result['node_id']
        relationship = result['relationship']
        model = result['prediction_model']
        print(id)

        results = []
        if (result['prediction_model'] != None):
            print(f"Prediction for {result['prediction_model']}:")

            predictions = predict_tail(id, relationship, model)
            # predictions_node_ids = predictions.head(5)['tail_label'].to_list()
            # print(f"Predictions: {predictions_node_ids")
            print(predictions)

            predictions_str_array = []
            for p in predictions:
                predictions_str_array.append(str(p))
                print(str(p))

            predictions_str = f"[{','.join(predictions_str_array)}]"

            # Query multiple entities by ids array MATCH (a) WHERE id(a) IN [1,2,4] RETURN a
            results = neomodel.db.cypher_query(
                f"MATCH (a) WHERE id(a) IN {predictions_str} RETURN a", resolve_objects=True)[0]
            print(results)
            data = {
                'response': {
                    'status': '200',
                    'data': [item[0].serialize for item in results]
                },
            }
        else:
            results = neomodel.db.cypher_query(
                f"MATCH (a)-[:{relationship}]-(b) WHERE id(a) = {id} RETURN b", resolve_objects=True)[0]

            data = {
                'response': {
                    'status': '200',
                    'data': [item[0].serialize for item in results]
                },
            }
        return Response(data)


class GetPOINodes(APIView):
    def get(self, request):
        count_info = {
            # 'node_type': request.GET.get('t', 'Entity'),
            'limit': request.GET.get('limit', ''),
        }

        poi_num = len(POI.nodes)
        pois = POI.nodes[0:poi_num]

        pois = POI.nodes.all()

        poi_data = [poi.serialize for poi in pois]
        data = {
            'response': {
                'status': '200',
                'data': poi_data,
            },
        }
        return Response(data)


class GetRoadNodes(APIView):
    def get(self, request):
        count_info = {
            # 'node_type': request.GET.get('t', 'Entity'),
            'limit': request.GET.get('limit', ''),
        }

        roads = Road.nodes.all()

        roads_data = [road.serialize for road in roads]
        data = {
            'response': {
                'status': '200',
                'data': roads_data,
            },
        }
        return Response(data)


class GetIncidentNodes(APIView):
    def get(self, request):
        count_info = {
            # 'node_type': request.GET.get('t', 'Entity'),
            'limit': request.GET.get('limit', ''),
        }

        incidents = Incident.nodes.all()

        incident_data = [incident.serialize for incident in incidents]
        data = {
            'response': {
                'status': '200',
                'data': incident_data,
            },
        }
        return Response(data)


class GetSpeedRangeNodes(APIView):
    def get(self, request):
        count_info = {
            'node_type': request.GET.get('node_type', 'Entity'),
            'date': request.GET.get('date', ''),
            'time': request.GET.get('time', ''),
            'range_start': request.GET.get('range_start', ''),
            'range_end': request.GET.get('range_end', ''),
            'limit': request.GET.get('limit', ''),
        }

        range_start = count_info['range_start']
        range_end = count_info['range_end']
        node_type = count_info['node_type']

        date = count_info['date']
        time = count_info['time']

        response_data = []

        if node_type == 'Road' and date != '' and time != '':
            print(f"Filter for date: {date} time: {time}")
            results = neomodel.db.cypher_query(
                f"MATCH (r:Road)-[:ROAD_DATE]->(d:Date {{name:'{date}'}}), (d)-[:DATE_TIME]->(t:Time{{name:'{time}'}}), (t)-[:HAS_TRAFFIC_SITUATION]->(tr:TrafficSituation WHERE (tr.speed >= {range_start} AND tr.speed <= {range_end})) RETURN r LIMIT 1000", resolve_objects=True)[0]
            response_data = [road[0].serialize for road in results]
        elif node_type == 'Road':
            results = neomodel.db.cypher_query(
                f"MATCH (r:Road)-[:ROAD_DATE]->(d:Date), (d)-[:DATE_TIME]->(t:Time), (t)-[:HAS_TRAFFIC_SITUATION]->(tr:TrafficSituation WHERE (tr.speed >= {range_start} AND tr.speed <= {range_end})) RETURN r LIMIT 1000", resolve_objects=True)[0]
            response_data = [road[0].serialize for road in results]
        
        data = {
            'response': {
                'status': '200',
                'data': response_data,
            },
        }
        return Response(data)



class GetDateNodes(APIView):
    def get(self, request):
        count_info = {
            'limit': request.GET.get('limit', ''),
        }

        date_nodes = Date.nodes.all()
        response_data = [node.serialize for node in date_nodes]
        data = {
            'response': {
                'status': '200',
                'data': response_data,
            },
        }
        return Response(data)
    

class GetTimeNodes(APIView):
    def get(self, request):
        count_info = {
            'limit': request.GET.get('limit', ''),
        }

        time_nodes = Time.nodes.all()
        response_data = [node.serialize for node in time_nodes]
        data = {
            'response': {
                'status': '200',
                'data': response_data,
            },
        }
        return Response(data)
