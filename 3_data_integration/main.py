from data_integration import Neo4JIntegration


if __name__ == "__main__":
    connection = Neo4JIntegration("bolt://localhost:7687", "neo4j", "kgtransport")
    connection.createEntities()
    # connection.createRelationships()
    connection.close()