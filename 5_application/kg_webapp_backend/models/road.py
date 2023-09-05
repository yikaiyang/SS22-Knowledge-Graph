from neomodel import (config, StructuredNode, StringProperty,
                      IntegerProperty, FloatProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty)

from kg_webapp_backend.util import element_id_to_node_id


class Road(StructuredNode):
    node_id = StringProperty()
    latitude = FloatProperty()
    longitude = FloatProperty()
    length = IntegerProperty()
    name = StringProperty()

    # connected_roads = RelationshipTo('.road.Road', 'IS_CONNECTED')

    # poi = RelationshipFrom('.poi.POI', 'IS_LOCATED')
    # incidents = RelationshipFrom('.incident.Incident', 'IS_NEARBY')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'entity_type': __class__.__name__,
                'node_id': element_id_to_node_id(self.element_id),
                'latitude': self.latitude,
                'longitude': self.longitude,
                'length': self.length,
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
    #             'nodes_type': 'POI',
    #             'nodes_related': self.serialize_relationships(self.poi.all()),
    #         },
    #         {
    #             'nodes_type': 'Incident',
    #             'nodes_related': self.serialize_relationships(self.incidents.all()),
    #         }
    #     ]
