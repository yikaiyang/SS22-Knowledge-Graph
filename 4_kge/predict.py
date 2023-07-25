#from pykeen.models import predict
import torch
from pykeen.triples import TriplesFactory
from pykeen import predict
from pathlib import Path
from typing import Literal
from pykeen.utils import set_random_seed

tf = TriplesFactory.from_path_binary('/Users/yikaiyang/Projects/SS22-Knowledge-Graph/4_kge/triples')
working_dir = Path(__file__).parent

PATH = '/Users/yikaiyang/Projects/SS22-Knowledge-Graph/4_kge/results/RotatE/trained_model.pkl'

set_random_seed(0)

def predict_tail():
    model = torch.load(PATH)
    pred = predict.predict_target(
        model,
        head=0,
        relation='HAS_INCIDENT',
        triples_factory= tf
    )
    # pred = predict.get_tail_prediction_df(
    #     model, 
    #     tf,
    #     '0',
    #     'HAS_INCIDENT'
    # )
    print(pred.df['tail_label'])

predict_tail()