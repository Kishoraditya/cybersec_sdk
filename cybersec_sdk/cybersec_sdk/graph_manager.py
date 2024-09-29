# cybersec_sdk/graph_manager.py

import networkx as nx
from typing import List, Dict

class GraphManager:
    """
    Manages the creation and manipulation of the system graph database.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_processes(self, processes: List[Dict]):
        """
        Adds processes to the graph.
        """
        for proc in processes:
            self.graph.add_node(proc['pid'], type='process', **proc)

    def add_connections(self, connections: List[Dict]):
        """
        Adds network connections to the graph.
        """
        for conn in connections:
            self.graph.add_node(conn['fd'], type='connection', **conn)
            if conn['pid']:
                self.graph.add_edge(conn['pid'], conn['fd'], relation='uses')

    def add_users(self, users: List[Dict]):
        """
        Adds users to the graph.
        """
        for user in users:
            self.graph.add_node(user['name'], type='user', **user)

    def build_relations(self):
        """
        Builds relationships between users, processes, and connections.
        """
        for node_id, data in self.graph.nodes(data=True):
            if data['type'] == 'process':
                user = data.get('username')
                if user and self.graph.has_node(user):
                    self.graph.add_edge(user, node_id, relation='owns')

    def export_graph(self, path: str):
        """
        Exports the graph to a file.
        """
        nx.write_gexf(self.graph, path)
