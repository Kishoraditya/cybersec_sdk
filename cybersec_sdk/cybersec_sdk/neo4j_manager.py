# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/

# cybersec_sdk/neo4j_manager.py
import os
from neo4j import GraphDatabase
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class Neo4jManager:
    """
    Manages the connection and operations with Neo4j graph database.
    """

    def __init__(self, uri=None, user=None, password=None):
        uri = uri or os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
        user = user or os.environ.get('NEO4J_USER', 'neo4j')
        password = password or os.environ.get('NEO4J_PASSWORD', "Qwerty@123")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label: str, properties: Dict):
        try:
            with self.driver.session() as session:
                session.write_transaction(self._create_and_return_node, label, properties)
        except Exception as e:
            logger.error(f"Error creating node {label} with properties {properties}: {e}")

    @staticmethod
    def _create_and_return_node(tx, label: str, properties: Dict):
        #prop_str = ', '.join([f"{k}: ${k}" for k in properties.keys()])
        #query = f"MERGE (n:{label} {{ {prop_str} }}) RETURN n"
        #tx.run(query, **properties)
        query = f"""
            MERGE (n:{label} {{id: $id}})
            ON CREATE SET n = $props
            ON MATCH SET n += $props
            RETURN n
            """
        tx.run(query, id=properties['id'], props=properties)

    def create_relationship(self, from_id, to_id, relation: str):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_relationship, from_id, to_id, relation)

    @staticmethod
    def _create_and_return_relationship(tx, from_id, to_id, relation: str):
        query = (
            #"MATCH (a {id: $from_id}) OPTIONAL MATCH (b {id: $to_id}) CREATE (a)-[r:USES]->(b)RETURN r"
             f"""
            MATCH (a {{id: $from_id}})
            MATCH (b {{id: $to_id}})
            MERGE (a)-[r:{relation}]->(b)
            RETURN r
            """
        )
        tx.run(query, from_id=from_id, to_id=to_id)

    def run_query(self, query: str, parameters: Dict = None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            #return [record for record in result]
            return [record.data() for record in result]
