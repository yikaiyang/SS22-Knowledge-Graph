from rest_framework.views import APIView
from rest_framework.response import Response
from models.poi import POI
from models.road import Road
from models.incident import Incident
from models.datetime import DateTime
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
            #predictions_node_ids = predictions.head(5)['tail_label'].to_list()
            #print(f"Predictions: {predictions_node_ids")
            print(predictions)

            predictions_str_array = []
            for p in predictions:
                predictions_str_array.append(str(p))
                print(str(p))

            predictions_str = f"[{','.join(predictions_str_array)}]"
           
            # Query multiple entities by ids array MATCH (a) WHERE id(a) IN [1,2,4] RETURN a 
            results = neomodel.db.cypher_query(f"MATCH (a) WHERE id(a) IN {predictions_str} RETURN a", resolve_objects=True)[0]
            print(results)
            data = {
                'response': {
                    'status': '200',
                    'data': [item[0].serialize for item in results]
                },
            }
        else:
            results = neomodel.db.cypher_query(f"MATCH (a)-[:{relationship}]-(b) WHERE id(a) = {id} RETURN b", resolve_objects=True)[0]
   
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
            #'node_type': request.GET.get('t', 'Entity'),
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
            #'node_type': request.GET.get('t', 'Entity'),
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
            #'node_type': request.GET.get('t', 'Entity'),
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