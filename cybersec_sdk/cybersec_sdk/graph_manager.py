# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/

# cybersec_sdk/graph_manager.py

from typing import List, Dict
from .neo4j_manager import Neo4jManager
import psutil

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GraphManager:
    """
    Manages the creation and manipulation of the system graph database using Neo4j.
    """

    def __init__(self, neo4j_manager: Neo4jManager):
        self.neo4j_manager = neo4j_manager
        self._create_constraints()
        
    def _create_constraints(self):
        # Add uniqueness constraints
        queries = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Process) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Connection) REQUIRE c.id IS UNIQUE",
        ]
        for query in queries:
            self.neo4j_manager.run_query(query)

    def add_processes(self, processes: List[Dict]):
        for proc in processes:
            proc['pid'] = int(proc['pid'])
            properties = {
                'id': str(proc['pid']),
                **proc,
                'type': 'Process'
            }
            self.neo4j_manager.create_node('Process', properties)

    def add_connections(self, connections: List[Dict]):
        for conn in connections:
            # Sanitize the connection data
            sanitized_conn = self._sanitize_data(conn)
            
            # Generate a unique ID for the connection
            local_addr = sanitized_conn.get('laddr', 'unknown')
            remote_addr = sanitized_conn.get('raddr', 'unknown')
            pid = sanitized_conn.get('pid', 'unknown')
            conn_type = sanitized_conn.get('type', 'unknown')
            node_id = f"conn_{pid}_{local_addr}_{remote_addr}_{conn_type}"
            
            properties = {
                'id': node_id,
                **sanitized_conn,
                'type': 'Connection'
            }
            self.neo4j_manager.create_node('Connection', properties)
            if pid != 'unknown':
                self.neo4j_manager.create_relationship(
                    from_id=str(pid),
                    to_id=node_id,
                    relation='USES'
                )


    def add_users(self, users: List[Dict]):
        for user in users:
            node_id = f"{user['name']}@{user['host']}" 
            properties = {
                'id': node_id,
                **user,
                'type': 'User'
            }
            self.neo4j_manager.create_node('User', properties)

    def build_relations(self):
        # Build relations between users and processes
        query = """
        MATCH (u:User)
        MATCH (p:Process {username: u.name})
        MERGE (u)-[:OWNS]->(p)
        """
        self.neo4j_manager.run_query(query)

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

    def close(self):
        self.neo4j_manager.close()
