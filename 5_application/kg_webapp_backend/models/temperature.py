from neomodel import (config, StructuredNode, StringProperty,
                      IntegerProperty, FloatProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty)

from .nodeutils import NodeUtils

class Temperature(StructuredNode, NodeUtils):
    node_id = UniqueIdProperty()
    name = FloatProperty()
    
    connected_roads = RelationshipTo('.road.Road', 'IS_CONNECTED')
    
    date_time = RelationshipFrom('datetime.DateTime', 'HAS_TEMPERATURE')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'node_id': self.node_id,
                'name': self.name
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
