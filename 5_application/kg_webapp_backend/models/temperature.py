from neomodel import (config, StructuredNode, StringProperty,
                      IntegerProperty, FloatProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty)
from kg_webapp_backend.util import element_id_to_node_id

class Temperature(StructuredNode):
    # node_id = StringProperty()
    name = FloatProperty()
    
    # connected_roads = RelationshipTo('.road.Road', 'IS_CONNECTED')
    
    # date_time = RelationshipFrom('datetime.DateTime', 'HAS_TEMPERATURE')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'entity_type': __class__.__name__,
                'node_id': element_id_to_node_id(self.element_id),
                'name': self.name
            },
        }

    # @property
    # def serialize_connections(self):
    #     return [
    #         {
    #             'nodes_type': 'Road',
    #             'nodes_related': self.serialize_relationships(self.connected_roads.all()),
    #         },
    #         {
    #             'nodes_type': 'DateTime',
    #             'nodes_related': self.serialize_relationships(self.date_time.all()),
    #         }
    #     ]
