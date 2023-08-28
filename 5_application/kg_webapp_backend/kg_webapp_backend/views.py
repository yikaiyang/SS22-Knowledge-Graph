from rest_framework.views import APIView
from rest_framework.response import Response
from models.poi import POI
from models.road import Road
from models.incident import Incident

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