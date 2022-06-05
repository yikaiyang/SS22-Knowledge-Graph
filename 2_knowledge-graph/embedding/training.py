#https://analyticsindiamag.com/complete-guide-to-pykeen-python-knowledge-embeddings-for-knowledge-graphs/

from pykeen.datasets import OpenBioLink
from pykeen.models import TransE
from torch.optim import Adam
from pykeen.training import SLCWATrainingLoop
# Pick an evaluator 
from pykeen.evaluation import RankBasedEvaluator
dataset = OpenBioLink()
training_triples_factory = dataset.training

# Pick a model
model = TransE(triples_factory=training_triples_factory)
# Pick an optimizer from Torch
optimizer = Adam(params=model.get_grad_params())

# Pick a training approach (sLCWA or LCWA)
training_loop = SLCWATrainingLoop(
    model=model, 
    triples_factory = training_triples_factory,
    optimizer=optimizer
)
training_loop.train(
    triples_factory=training_triples_factory,
    num_epochs=5, 
    batch_size=256)

evaluator = RankBasedEvaluator()
# Get triples to test
mapped_triples = dataset.testing.mapped_triples
# Evaluate
results = evaluator.evaluate(model, mapped_triples, batch_size=1024)
print(results)