from neomodel import (config, StructuredNode, StringProperty,
                      IntegerProperty, FloatProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty)

from .nodeutils import NodeUtils

class Weather(StructuredNode, NodeUtils):
    node_id = UniqueIdProperty()
    name = StringProperty()
    date_time = RelationshipFrom('DateTime', 'HAS_TEMPERATURE')

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
                'nodes_type': 'DateTime',
                'nodes_related': self.serialize_relationships(self.date_time.all()),
            }
        ]


