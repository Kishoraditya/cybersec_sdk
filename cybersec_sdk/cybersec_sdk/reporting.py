# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/

# cybersec_sdk/reporting.py

import json
from typing import Dict
from .analyzer import SystemAnalyzer
from .graph_manager import GraphManager

class ReportGenerator:
    """
    Generates reports from analysis data.
    """

    def __init__(self, analyzer: SystemAnalyzer, graph_manager: GraphManager):
        self.analyzer = analyzer
        self.graph_manager = graph_manager

    def generate_summary(self) -> Dict:
        """
        Generates a summary report.
        """
        summary = {
            'processes': len(self.analyzer.get_running_processes()),
            'users': len(self.analyzer.get_users()),
            'connections': len(self.analyzer.get_network_connections()),
            'vulnerabilities': len(self.analyzer.identify_vulnerabilities())
        }
        return summary

    def export_report(self, path: str):
        """
        Exports the summary report to a JSON file.
        """
        summary = self.generate_summary()
        with open(path, 'w') as f:
            json.dump(summary, f, indent=4)
