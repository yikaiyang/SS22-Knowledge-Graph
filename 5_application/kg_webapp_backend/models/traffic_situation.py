from neomodel import (config, StructuredNode, StringProperty,
                      IntegerProperty, FloatProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty)


from .nodeutils import NodeUtils

class TrafficSituation(StructuredNode, NodeUtils):
    node_id = UniqueIdProperty()
    speed = IntegerProperty()

    connected_roads = RelationshipTo('.road.Road', 'IS_CONNECTED')
    
    date_time = RelationshipFrom('.datetime.DateTime', 'HAS_TRAFFIC_SITUATION')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'node_id': self.node_id,
                'speed': self.speed
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Road',
                'nodes_related': self.serialize_relationships(self.connected_roads.all()),
            },
            {
                'nodes_type': 'DateTime',
                'nodes_related': self.serialize_relationships(self.date_time.all()),
            }
        ]
