from neomodel import (config, StructuredNode, StringProperty,
                      IntegerProperty, FloatProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty)

from kg_webapp_backend.util import element_id_to_node_id

class Incident(StructuredNode):
    node_id = StringProperty()
    criticality = StringProperty()
    incident_type = StringProperty(db_property='incidentType')
    name = StringProperty()
    latitude = FloatProperty()
    longitude = FloatProperty()

    # date_time = RelationshipFrom('.datetime.DateTime', 'HAS_INCIDENT')
 
    @property
    def serialize(self):
        return {
            'node_properties': {
                'entity_type': __class__.__name__,
                'node_id': element_id_to_node_id(self.element_id),
                'criticality': self.criticality,
                'incident_type': self.incident_type,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'name': self.name
            },
        }

    # @property
    # def serialize_connections(self):
    #     return [
    #         {
    #             'nodes_type': 'DateTime',
    #             'nodes_related': self.serialize_relationships(self.date_time.all()),
    #         }
    # ]
