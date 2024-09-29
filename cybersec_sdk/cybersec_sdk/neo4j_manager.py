# cybersec_sdk/neo4j_manager.py

from neo4j import GraphDatabase
from typing import Dict

class Neo4jManager:
    """
    Manages the connection and operations with Neo4j graph database.
    """

    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="Qwerty@123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label: str, properties: Dict):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_node, label, properties)

    @staticmethod
    def _create_and_return_node(tx, label: str, properties: Dict):
        prop_str = ', '.join([f"{k}: ${k}" for k in properties.keys()])
        query = f"CREATE (n:{label} {{ {prop_str} }}) RETURN n"
        tx.run(query, **properties)

    def create_relationship(self, from_id, to_id, relation: str):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_relationship, from_id, to_id, relation)

    @staticmethod
    def _create_and_return_relationship(tx, from_id, to_id, relation: str):
        query = (
            "MATCH (a {id: $from_id}), (b {id: $to_id}) "
            f"CREATE (a)-[r:{relation}]->(b) RETURN r"
        )
        tx.run(query, from_id=from_id, to_id=to_id)
        
    def run_query(self, query: str, parameters: Dict = None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]
