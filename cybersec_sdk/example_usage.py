# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/

# example_usage.py

from cybersec_sdk import SystemAnalyzer, GraphManager, Neo4jManager, ReportGenerator
from cybersec_sdk.ml_models import AnomalyDetector
from cybersec_sdk.ai_assistant import AIAssistant
from cybersec_sdk.ui import run_ui
from cybersec_sdk.external_data import ThreatIntelFeed
import pandas as pd
import subprocess
import os

def main():
    # Initialize components
    analyzer = SystemAnalyzer()
    neo4j_manager = Neo4jManager(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="Qwerty@123"  # Replace with your actual password or use environment variables
    )
    graph_manager = GraphManager(neo4j_manager)

    # Perform system analysis
    processes = analyzer.get_running_processes()
    users = analyzer.get_users()
    connections = analyzer.get_network_connections()
    open_files = analyzer.get_open_files()
    vulnerabilities = analyzer.identify_vulnerabilities()

    # Build the graph in Neo4j
    graph_manager.add_processes(processes)
    graph_manager.add_users(users)
    graph_manager.add_connections(connections)
    graph_manager.build_relations()

    df_processes = pd.DataFrame(processes)
    features = ['cpu_percent', 'memory_percent', 'num_threads']
    df_features = df_processes[features].fillna(0)

    # Initialize and train the anomaly detector
    anomaly_detector = AnomalyDetector()
    anomaly_detector.train(df_features)

    # Predict anomalies
    df_processes['anomaly'] = anomaly_detector.predict(df_features)

    # Identify anomalous processes
    anomalies = df_processes[df_processes['anomaly'] == -1]
    print(f"Detected {len(anomalies)} anomalous processes.")

    # Initialize AI Assistant
    ai_assistant = AIAssistant()  # No need to pass API key here; it's configured in the class

    # Generate explanations for anomalies
    for _, row in anomalies.iterrows():
        pid = int(row['pid'])
        result = neo4j_manager.run_query(
            "MATCH (p:Process {id: $id}) RETURN p",
            {'id': str(pid)}
        )
        if result:
            neo4j_manager.run_query(
                "MATCH (p:Process {id: $id}) SET p.anomaly = true",
                {'id': str(pid)}
            )
            # Generate explanation
            prompt = f"Explain why a process with PID {pid} named {row['name']} might be considered anomalous based on its CPU usage of {row['cpu_percent']}% and memory usage of {row['memory_percent']}%."
            explanation = ai_assistant.generate_explanation(prompt)
            # Update the process node with the explanation
            neo4j_manager.run_query(
                "MATCH (p:Process {id: $id}) SET p.explanation = $explanation",
                {'id': str(pid), 'explanation': explanation}
            )
        else:
            print(f"No Process node found for PID {pid}, anomaly property not set.")

    # Generate and export a report
    report_generator = ReportGenerator(analyzer, graph_manager)
    report_generator.export_report('system_report.json')

    # Launch the UI
    run_ui(neo4j_manager)

    # Clean up
    graph_manager.close()

if __name__ == '__main__':
    main()
