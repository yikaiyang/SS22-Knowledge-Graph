#from pykeen.models import predict
import torch
from pykeen.triples import TriplesFactory
from pykeen import predict
from pathlib import Path
from typing import Literal
from pykeen.utils import set_random_seed
import os
import pandas as pd


working_dir = Path(__file__).parent.parent
print(working_dir)

set_random_seed(0)

tf = TriplesFactory.from_path_binary('/Users/yikaiyang/Projects/SS22-Knowledge-Graph/4_kge/triples')


PATH = os.path.join(working_dir, '4_kge/results/RotatE/trained_model.pkl')

entity_to_id_file_path = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/4_kge/triples/entity_to_id.tsv'

# Converts an neo4j id to an entity id.
def entity_to_id(entity_id):
    df = pd.read_csv(entity_to_id_file_path, sep='\t')
    row = df.loc[df['label'] == entity_id]
    value = row['id'].iloc[0]
    return value

def predict_tail(head_node_id, relationship):
    model = torch.load(PATH)
    pred = predict.predict_target(
        model,
        head=head_node_id,
        relation=relationship,
        triples_factory= tf
    )

    print(pred.df['tail_label'])
    return pred

### I am not sure why the conversion of neo4j node ids to pykeen internal ids seems to be broken. 
# For now it seems that a monkey patch in the form of a custom method 'entity_to_id' is necessary
#a = tf.entities_to_ids([3034]) Does not work
a = entity_to_d(3034)

print(a)
#result = predict_tail(2094, 'HAS_INCIDENT')
#print(result)