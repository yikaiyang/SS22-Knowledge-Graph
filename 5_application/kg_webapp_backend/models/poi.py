from neomodel import (config, StructuredNode, StringProperty,
                      IntegerProperty, FloatProperty, RelationshipTo, UniqueIdProperty)

config.DATABASE_URL = 'bolt://neo4j:kgtransport@localhost:7687/neo4j'

from .nodeutils import NodeUtils

class POI(StructuredNode, NodeUtils):
    node_id =  UniqueIdProperty()
    latitude = FloatProperty()
    longitude = FloatProperty()
    name = StringProperty()
    category = StringProperty()

    is_located = RelationshipTo('.road.Road', 'IS_LOCATED')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'node_id': self.element_id,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'name': self.name,
                'category': self.category
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'Road',
                'nodes_related': self.serialize_relationships(self.is_located.all()),
            }
        ]