from neomodel import (config, StructuredNode, StringProperty,
                      IntegerProperty, FloatProperty, RelationshipTo, UniqueIdProperty)

from kg_webapp_backend.util import element_id_to_node_id

class POI(StructuredNode):
    node_id =  StringProperty()
    latitude = FloatProperty()
    longitude = FloatProperty()
    name = StringProperty()
    category = StringProperty()

    # is_located = RelationshipTo('.road.Road', 'IS_LOCATED')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'entity_type': __class__.__name__,
                'node_id': element_id_to_node_id(self.element_id),
                'latitude': self.latitude,
                'longitude': self.longitude,
                'name': self.name,
                'category': self.category
            },
        }

    # @property
    # def serialize_connections(self):
    #     return [
    #         {
    #             'nodes_type': 'Road',
    #             'nodes_related': self.serialize_relationships(self.is_located.all()),
    #         }
    #     ]