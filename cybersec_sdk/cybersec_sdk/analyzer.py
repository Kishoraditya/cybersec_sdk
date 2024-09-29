# cybersec_sdk/analyzer.py

import psutil
from typing import List, Dict

class SystemAnalyzer:
    """
    Analyzes the host system to identify actors, processes, and vulnerabilities.
    """

    def __init__(self):
        pass

    def get_running_processes(self) -> List[Dict]:
        """
        Retrieves a list of currently running processes.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes

    def get_network_connections(self) -> List[Dict]:
        """
        Retrieves active network connections.
        """
        connections = []
        for conn in psutil.net_connections():
            connections.append({
                'fd': conn.fd,
                'family': str(conn.family),
                'type': str(conn.type),
                'laddr': conn.laddr,
                'raddr': conn.raddr,
                'status': conn.status,
                'pid': conn.pid
            })
        return connections

    def get_users(self) -> List[Dict]:
        """
        Retrieves logged-in users.
        """
        users = []
        for user in psutil.users():
            users.append({
                'name': user.name,
                'terminal': user.terminal,
                'host': user.host,
                'started': user.started
            })
        return users
