import re

#input_string = "4:01c73c9a-aa6d-420a-96a7-3c39c7f51ewwerfc:2806"   -> extracts 2806
pattern = r"^(?:[^:]*:){2}([^:]+)"

def element_id_to_node_id(element_id):
    match = re.match(pattern, element_id)
    if match:
        third_column = match.group(1)
        return third_column
