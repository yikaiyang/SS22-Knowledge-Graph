from neomodel import (config, StructuredNode, StringProperty,
                      IntegerProperty, FloatProperty, RelationshipTo, RelationshipFrom, UniqueIdProperty)


from .nodeutils import NodeUtils

class Incident(StructuredNode, NodeUtils):
    node_id = UniqueIdProperty()
    criticality = StringProperty()
    incident_type = StringProperty()
    name = StringProperty()

    date_time = RelationshipFrom('.datetime.DateTime', 'HAS_INCIDENTS')
    traffic_situations = RelationshipTo('.traffic_situation.TrafficSituation', 'HAS_TRAFFIC_SITUATION')

    @property
    def serialize(self):
        return {
            'node_properties': {
                'node_id': self.node_id,
                'criticality': self.criticality,
                'incident_type': self.incident_type,
                'name': self.name
            },
        }

    @property
    def serialize_connections(self):
        return [
            {
                'nodes_type': 'DateTime',
                'nodes_related': self.serialize_relationships(self.date_time.all()),
            },
            {
                'nodes_type': 'TrafficSituation',
                'nodes_related': self.serialize_relationships(self.traffic_situations.all()),
            }
    ]
