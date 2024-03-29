# Extracts Pykeen triples from Neo4J database as seen in:
# https://towardsdatascience.com/knowledge-graph-completion-with-pykeen-and-neo4j-6bca734edf43

# Define Neo4j connections
from neo4j import GraphDatabase
import pandas as pd
from pykeen.triples import TriplesFactory
from pathlib import Path
import os

host = 'bolt://localhost:7687'
user = 'neo4j'
password = 'kgtransport'
driver = GraphDatabase.driver(host,auth=(user, password))   

WORKING_DIR = Path(__file__).parent
TRIPLES_PATH = os.path.join(WORKING_DIR, 'triples')


def run_query(query, params={}):
    with driver.session() as session:
        result = session.run(query, params)
        return pd.DataFrame([r.values() for r in result], columns=result.keys())

def extract_triples_from_db():
  data = run_query("""
      MATCH (s)-[r]->(t)
      RETURN toString(id(s)) as source, toString(id(t)) AS target, type(r) as type
      """)

  tf = TriplesFactory.from_labeled_triples(
    data[["source", "type", "target"]].values
  )

  tf.to_path_binary(TRIPLES_PATH)