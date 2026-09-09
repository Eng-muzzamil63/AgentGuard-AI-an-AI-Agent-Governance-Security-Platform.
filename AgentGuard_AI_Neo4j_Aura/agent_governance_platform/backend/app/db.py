from neo4j import GraphDatabase
from .config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE

_driver = None

def driver():
    global _driver
    if _driver is None:
        if not NEO4J_URI or not NEO4J_PASSWORD:
            raise RuntimeError("Neo4j Aura credentials are not configured. Copy .env.example to .env and fill them in.")
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    return _driver

def run(query, params=None):
    with driver().session(database=NEO4J_DATABASE) as session:
        return [dict(r) for r in session.run(query, params or {})]
