from neomodel import ( StructuredNode, StringProperty,
                      IntegerProperty)
from kg_webapp_backend.util import element_id_to_node_id

class Date(StructuredNode):
    node_id =  StringProperty()
    day = IntegerProperty()
    month = IntegerProperty()
    year = IntegerProperty()
    name = StringProperty()

    @property
    def serialize(self):
        return {
            'node_properties': {
                'entity_type': __class__.__name__,
                'node_id': element_id_to_node_id(self.element_id),
                'day': self.day,
                'month': self.month,
                'year': self.year,
                'name': self.name
            },
        }

    # @property
    # def serialize_connections(self):
    #     return [
    #         {
    #             'nodes_type': 'Incident',
    #             'nodes_related': self.serialize_relationships(self.incidents.all()),
    #         },
    #         {
    #             'nodes_type': 'Traffic Situations',
    #             'nodes_related': self.serialize_relationships(self.traffic_situations.all()),
    #         },
    #         {
    #             'nodes_type': 'Weather',
    #             'nodes_related': self.serialize_relationships(self.weather.all()),
    #         },
    #         {
    #             'nodes_type': 'Temperature',
    #             'nodes_related': self.serialize_relationships(self.temperature.all()),
    #         },
    # ]

