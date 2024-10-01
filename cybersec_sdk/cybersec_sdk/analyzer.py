# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/

# cybersec_sdk/analyzer.py

import psutil
from typing import List, Dict
import time

class SystemAnalyzer:
    """
    Analyzes the host system to identify actors, processes, and vulnerabilities.
    """

    def __init__(self):
        pass

    def get_running_processes(self) -> List[Dict]:
        """
        Retrieves a list of running processes with their details.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'num_threads']):
            try:
                if proc.pid in [0, 4]:
                    continue
                # Initial call to collect CPU usage
                proc.cpu_percent(interval=0)
                # Sleep for a short interval
                time.sleep(1)
                # Second call to get the actual CPU usage
                cpu_percent = proc.cpu_percent(interval=None)
                proc_info = {
                    'pid': proc.pid,
                    'name': proc.name(),
                    'username': proc.username() if proc.username() else "Unknown",
                    'cpu_percent': cpu_percent,
                    'memory_percent': proc.memory_percent(),
                    'num_threads': proc.num_threads(),
                }
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return processes



    def get_network_connections(self) -> List[Dict]:
        """
        Retrieves a list of network connections with sanitized data.
        """
        connections = psutil.net_connections()
        conn_list = []
        for conn in connections:
            conn_dict = conn._asdict()
            sanitized_conn = self._sanitize_connection(conn_dict)
            conn_list.append(sanitized_conn)
        return conn_list
    
    def _sanitize_connection(self, conn: Dict) -> Dict:
        sanitized = {}
        for key, value in conn.items():
            if key in ('laddr', 'raddr'):
                if isinstance(value, tuple) and len(value) >= 2:
                    sanitized[key] = f"{value[0]}:{value[1]}"
                else:
                    sanitized[key] = 'unknown'
            elif isinstance(value, psutil._common.addr):
                sanitized[key] = f"{value.ip}:{value.port}" if value else 'unknown'
            elif isinstance(value, (int, float, str, bool)) or value is None:
                sanitized[key] = value
            else:
                sanitized[key] = str(value)
        return sanitized


    def get_users(self) -> List[Dict]:
        """
        Retrieves a list of users logged into the system.
        """
        users = psutil.users()
        user_list = []
        for user in users:
            user_list.append({
                'name': user.name,
                'terminal': user.terminal,
                'host': user.host,
                'started': user.started
            })
        return user_list
    
    def get_open_files(self) -> List[Dict]:
        """
        Retrieves a list of open files.
        """
        open_files = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                files = proc.open_files()
                for file in files:
                    open_files.append({
                        'pid': proc.pid,
                        'process_name': proc.name(),
                        'file': file.path
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
        
