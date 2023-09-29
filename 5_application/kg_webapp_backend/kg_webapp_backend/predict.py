#from pykeen.models import predict
import torch
from pykeen.triples import TriplesFactory
from pykeen import predict
from pathlib import Path
from pykeen.utils import set_random_seed
import os
import pandas as pd


working_dir = Path(__file__).parent.parent.parent.parent
print(working_dir)

set_random_seed(0)

PATH = os.path.join(working_dir, '4_kge/results/RotatE/trained_model.pkl')
TRIPLES_PATH = os.path.join(working_dir, '4_kge/triples')

ENTITY_TO_ID_FILE_PATH = os.path.join(working_dir, '4_kge/triples/entity_to_id.tsv')

tf = TriplesFactory.from_path_binary(TRIPLES_PATH)

def get_model_path(model_name):
    return os.path.join(working_dir, f'4_kge/results/{model_name}/trained_model.pkl')

# Converts an neo4j id to an entity id.
def entity_to_id(entity_id):
    df = pd.read_csv(ENTITY_TO_ID_FILE_PATH, sep='\t')
    row = df[df['label'] == entity_id]
    value = None
    if not row.empty:
        print(row['id'])
        value = row['id'].iloc[0]
    return value

def predict_tail(head_node_id, relationship, model_name):
    path = get_model_path(model_name)

    head_node_id = int(head_node_id)
    pykeen_id = head_node_id 
    #pykeen_id = entity_to_id(head_node_id)
    pred = None
    if pykeen_id is not None:
        model = torch.load(path)
        pred = predict.predict_target(
            model,
            head=pykeen_id,
            relation=relationship,
            triples_factory= tf
        )
        pred = pred.df['tail_label'].head(5).to_list()
    return pred

