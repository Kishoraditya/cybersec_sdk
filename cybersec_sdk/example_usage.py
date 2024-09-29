# example_usage.py

from cybersec_sdk import SystemAnalyzer, GraphManager, Neo4jManager, ReportGenerator
import os
from cybersec_sdk.ml_models import AnomalyDetector
import pandas as pd
from cybersec_sdk.ai_assistant import AIAssistant
from cybersec_sdk.ui import run_ui
import subprocess
from cybersec_sdk.external_data import ThreatIntelFeed

def main():
    # Initialize components
    analyzer = SystemAnalyzer()
    neo4j_manager = Neo4jManager(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="Qwerty@123"
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
    # You can add open_files and vulnerabilities similarly if needed
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

    # You can now add anomalies to your graph or report
    # For example, tag anomalous processes in Neo4j
    for _, row in anomalies.iterrows():
        node_id = str(row['pid'])
        neo4j_manager.run_query(
            "MATCH (p:Process {id: $id}) SET p.anomaly = true",
            {'id': node_id}
        )
    # Initialize AI Assistant
    ai_assistant = AIAssistant(api_key='key here')  # Replace with your API key

    # Generate explanations for anomalies
    for _, row in anomalies.iterrows():
        prompt = f"Explain why a process with PID {row['pid']} named {row['name']} might be considered anomalous based on its CPU usage of {row['cpu_percent']}% and memory usage of {row['memory_percent']}%."
        explanation = ai_assistant.generate_explanation(prompt)
        print(f"Anomaly Explanation for PID {row['pid']}:\n{explanation}\n")

        # Optionally, store the explanation in Neo4j
        neo4j_manager.run_query(
            "MATCH (p:Process {id: $id}) SET p.explanation = $explanation",
            {'id': str(row['pid']), 'explanation': explanation}
        )

    # Generate and export a report
    report_generator = ReportGenerator(analyzer, graph_manager)
    report_generator.export_report('system_report.json')
    
    # Launch the UI
    run_ui(neo4j_manager)
    # Clean up
    graph_manager.close()
    # Launch Streamlit UI in a subprocess
    subprocess.run(["streamlit", "run", "cybersec_sdk/ui.py"])
    
    # Retrieve threat intelligence data
    feed = ThreatIntelFeed('https://api.threatintel.com/feeds/example')
    threat_data = feed.get_threat_data()

    # Process and integrate threat data
    for threat in threat_data:
        # For example, add malicious IPs to Neo4j
        ip = threat.get('malicious_ip')
        if ip:
            neo4j_manager.create_node('MaliciousIP', {'id': ip, 'ip': ip, 'type': 'MaliciousIP'})

    # Update relationships if necessary
    # For example, link connections to malicious IPs
    query = """
    MATCH (c:Connection), (m:MaliciousIP)
    WHERE c.raddr = m.ip
    MERGE (c)-[:CONNECTS_TO]->(m)
    """
    neo4j_manager.run_query(query)

if __name__ == '__main__':
    main()
