from pykeen.datasets import OpenBioLink
from pykeen.models import TransE
from torch.optim import Adam
from pykeen.training import SLCWATrainingLoop
from pykeen.evaluation import RankBasedEvaluator
from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pathlib import Path
import os
from pykeen.utils import set_random_seed

set_random_seed(0)


tf = TriplesFactory.from_path_binary('/Users/yikaiyang/Projects/SS22-Knowledge-Graph/4_kge/triples')
working_dir = Path(__file__).parent

EPOCHS = 2000
MODELS = ['TransE', 'TransH', 'TransD', 'RotatE']

def train(epochs=EPOCHS, models=MODELS):
    for model in models:
        training, testing = tf.split(
            random_state=0
        )
        print(training)
        result = pipeline(
            training=training,
            testing=testing,
            model=model,
            model_kwargs=dict(
                random_seed=0
            ),
            epochs=epochs,  # short epochs for testing - you should go higher
            random_seed=0
        )
        print(result)
        # result_path = os.path.join(working_dir, model)
        # if not os.path.exists(result_path):
        #     # Directory does not exist. Create directory
        #     os.mkdir(result_path)
        result.save_to_directory(os.path.join(working_dir, 'results', model))
    # training_triples_factory = dataset.training

    # # Pick a model
    # model = TransE(triples_factory=training_triples_factory)
    # # Pick an optimizer from Torch
    # optimizer = Adam(params=model.get_grad_params())

    # # Pick a training approach (sLCWA or LCWA) 
    # training_loop = SLCWATrainingLoop(
    #     model=model,
    #     triples_factory = training_triples_factory,
    #     optimizer=optimizer
    # )
    # training_loop.train(
    #     triples_factory=training_triples_factory,
    #     num_epochs=5,
    #     batch_size=256)

    # evaluator = RankBasedEvaluator()
    # # Get triples to test
    # mapped_triples = dataset.testing.mapped_triples
    # # Evaluate
    # results = evaluator.evaluate(model, mapped_triples, batch_size=1024)
    # print(results)

#train(models=['TransE', 'TransH', 'TransD', 'RotatE'])