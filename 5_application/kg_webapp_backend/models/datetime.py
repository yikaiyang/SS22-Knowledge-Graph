from neomodel import (config, StructuredNode, StringProperty,
                      IntegerProperty, FloatProperty, RelationshipTo, UniqueIdProperty)

config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'
from .nodeutils import NodeUtils

class DateTime(StructuredNode, NodeUtils):
    node_id = UniqueIdProperty()
    day = IntegerProperty()
    month = IntegerProperty()
    year = IntegerProperty()
    hour = IntegerProperty()
    minute = IntegerProperty()
    name = StringProperty()

    incidents = RelationshipTo('.incident.Incident', 'HAS_INCIDENTS')
    traffic_situations = RelationshipTo(
        '.traffic_situation.TrafficSituation', 'HAS_TRAFFIC_SITUATION')
    weather = RelationshipTo('.weather.Weather', 'HAS_WEATHER')
    temperature = RelationshipTo('.temperature.Temperature', 'HAS_TEMPERATURE')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'node_id': self.node_id,
                'day': self.day,
                'month': self.month,
                'year': self.year,
                'hour': self.hour,
                'minute': self.minute,
                'name': self.name
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Incident',
                'nodes_related': self.serialize_relationships(self.incidents.all()),
            },
            {
                'nodes_type': 'Traffic Situations',
                'nodes_related': self.serialize_relationships(self.traffic_situations.all()),
            },
            {
                'nodes_type': 'Weather',
                'nodes_related': self.serialize_relationships(self.weather.all()),
            },
            {
                'nodes_type': 'Temperature',
                'nodes_related': self.serialize_relationships(self.temperature.all()),
            },
    ]

