# cybersec_sdk/graph_manager.py

from typing import List, Dict
from .neo4j_manager import Neo4jManager
import psutil

class GraphManager:
    """
    Manages the creation and manipulation of the system graph database using Neo4j.
    """

    def __init__(self, neo4j_manager: Neo4jManager):
        self.neo4j_manager = neo4j_manager

    def add_processes(self, processes: List[Dict]):
        for proc in processes:
            node_id = str(proc['pid'])
            properties = {
                'id': node_id,
                **proc,
                'type': 'Process'
            }
            self.neo4j_manager.create_node('Process', properties)

    def add_connections(self, connections: List[Dict]):
        for conn in connections:
            sanitized_conn = self._sanitize_data(conn)
            node_id = f"conn_{sanitized_conn['fd']}"
            properties = {
                'id': node_id,
                **sanitized_conn,
                'type': 'Connection'
            }
            self.neo4j_manager.create_node('Connection', properties)
            if sanitized_conn.get('pid'):
                self.neo4j_manager.create_relationship(
                    from_id=str(sanitized_conn['pid']),
                    to_id=node_id,
                    relation='USES'
                )
    
    def _sanitize_data(self, data):
        """
        Recursively sanitize data by converting unsupported types to strings.
        """
        if isinstance(data, dict):
            return {k: self._sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        elif isinstance(data, psutil._common.addr):
            # Convert addr to string "ip:port"
            return f"{data.ip}:{data.port}" if data else None
        elif isinstance(data, (int, float, str, bool)) or data is None:
            return data
        else:
            # Convert any other unsupported type to string
            return str(data)
    
    
    def add_users(self, users: List[Dict]):
        for user in users:
            node_id = user['name']
            properties = {
                'id': node_id,
                **user,
                'type': 'User'
            }
            self.neo4j_manager.create_node('User', properties)

    def build_relations(self):
        # Build relations between users and processes
        query = """
        MATCH (u:User), (p:Process)
        WHERE p.username = u.name
        MERGE (u)-[:OWNS]->(p)
        """
        self.neo4j_manager.run_query(query)

    def close(self):
        self.neo4j_manager.close()
