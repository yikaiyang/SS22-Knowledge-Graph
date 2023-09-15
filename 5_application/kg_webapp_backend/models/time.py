from neomodel import ( StructuredNode, StringProperty,
                      IntegerProperty)
from kg_webapp_backend.util import element_id_to_node_id

class Time(StructuredNode):
    node_id =  StringProperty()
    hour = IntegerProperty()
    minute = IntegerProperty()
    name = StringProperty()

    @property
    def serialize(self):
        return {
            'node_properties': {
                'entity_type': __class__.__name__,
                'node_id': element_id_to_node_id(self.element_id),
                'hour': self.hour,
                'minute': self.minute,
                'name': self.name
            },
        }


