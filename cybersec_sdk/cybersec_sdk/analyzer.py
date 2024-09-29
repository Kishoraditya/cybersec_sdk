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
        connections = psutil.net_connections()
        conn_list = []
        for conn in connections:
            conn_dict = conn._asdict()
            sanitized_conn = self._sanitize_connection(conn_dict)
            conn_list.append(sanitized_conn)
        return conn_list
    
    def _sanitize_connection(self, conn: Dict) -> Dict:
        """
        Sanitizes the connection dictionary by converting unsupported data types.
        """
        sanitized = {}
        for key, value in conn.items():
            if isinstance(value, psutil._common.addr):
                # Convert address to a string "ip:port"
                sanitized[key] = f"{value.ip}:{value.port}" if value else None
            elif isinstance(value, (int, float, str, bool)) or value is None:
                sanitized[key] = value
            else:
                # Convert other unsupported types to string
                sanitized[key] = str(value)
        return sanitized

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
    
    def get_open_files(self) -> List[Dict]:
        """
        Retrieves a list of open files by processes.
        """
        open_files = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                files = proc.open_files()
                for f in files:
                    open_files.append({
                        'pid': proc.pid,
                        'process_name': proc.info['name'],
                        'file': f.path
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return open_files

    def identify_vulnerabilities(self) -> List[Dict]:
        """
        Analyzes the system to identify potential vulnerabilities.
        """
        vulnerabilities = []
        # Example: Check for processes running as root/administrator
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                if proc.info['username'] == 'root' or proc.info['username'] == 'Administrator':
                    vulnerabilities.append({
                        'pid': proc.pid,
                        'process_name': proc.info['name'],
                        'issue': 'Process running with elevated privileges'
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return vulnerabilities
    
    def get_disk_usage(self) -> Dict:
        """
        Retrieves disk usage statistics.
        """
        usage = psutil.disk_usage('/')
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent
        }

    def get_network_io(self) -> Dict:
        """
        Retrieves network I/O statistics.
        """
        io_counters = psutil.net_io_counters()
        return {
            'bytes_sent': io_counters.bytes_sent,
            'bytes_recv': io_counters.bytes_recv,
            'packets_sent': io_counters.packets_sent,
            'packets_recv': io_counters.packets_recv
        }
        
