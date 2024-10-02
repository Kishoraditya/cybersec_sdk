# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/

# cybersec_sdk/ui.py

import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
from .ai_assistant import AIAssistant
from pyvis.network import Network
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt

def display_actor_profiles(neo4j_manager):
    # Fetch users
    users = neo4j_manager.run_query("MATCH (u:User) RETURN u.id AS id, u.name AS name")
    st.subheader("Users")
    st.table(users)

    # Fetch processes
    processes = neo4j_manager.run_query("MATCH (p:Process) RETURN p.id AS pid, p.name AS name")
    st.subheader("Processes")
    st.table(processes)

    # Fetch connections
    connections = neo4j_manager.run_query("MATCH (c:Connection) RETURN c.id AS id, c.laddr AS local_address, c.raddr AS remote_address")
    st.subheader("Network Connections")
    st.table(connections)
    
def display_system_graph(neo4j_manager):
    # Fetch nodes and relationships from Neo4j
    nodes = neo4j_manager.run_query("MATCH (n) RETURN n")
    relationships = neo4j_manager.run_query("""
        MATCH (n)-[r]->(m) 
        RETURN n.id AS source, m.id AS target, TYPE(r) AS relationship
    """)
    
    # Create a NetworkX graph
    G = nx.DiGraph()
    
    # Add nodes to the graph
    for node in nodes:
        node_id = node['n']['id']
        node_label = node['n'].get('name', 'Unnamed Node')
        G.add_node(node_id, label=node_label)

    # Add edges to the graph
    for rel in relationships:
        G.add_edge(rel['source'], rel['target'], label=rel['relationship'])

    # Create PyVis network
    net = Network(height='600px', width='100%', notebook=False, directed=True)
    net.from_nx(G)
    
    # Draw the graph
    plt.figure(figsize=(12, 8))
    nx.draw(G, with_labels=True, node_color='skyblue', edge_color='gray', node_size=1500, font_size=10)
    st.pyplot(plt)

    # Generate HTML and display in Streamlit
    html_content = net.generate_html()
    st.components.v1.html(html_content, height=600)
    
def run_ui(neo4j_manager):
    st.title("Cybersecurity SDK Dashboard")

    # Display summary statistics
    processes = neo4j_manager.run_query("MATCH (p:Process) RETURN count(p) AS process_count")
    users = neo4j_manager.run_query("MATCH (u:User) RETURN count(u) AS user_count")
    #anomalies = neo4j_manager.run_query("MATCH (p:Process) WHERE p.anomaly = true RETURN count(p) AS anomaly_count")
    anomalies = neo4j_manager.run_query(
        "MATCH (p:Process) WHERE p.anomaly = true RETURN p.id AS pid, p.name AS name, p.cpu_percent AS cpu_percent, p.memory_percent AS memory_percent, p.explanation AS explanation, count(p) AS anomaly_count"
    )
    anomalies_list = [record for record in anomalies]
    
    st.metric("Total Processes", processes[0]['process_count'])
    st.metric("Total Users", users[0]['user_count'])
    st.metric("Anomalous Processes", anomalies[0]['anomaly_count'])
    display_actor_profiles(neo4j_manager)
    display_system_graph(neo4j_manager)
    # Generate and display a summary using Gemini AI
    ai_assistant = AIAssistant()
    summary_prompt = "Provide a brief summary of the current system security status based on the following detected anomalies:\n\n"
    for anomaly in anomalies_list:
        summary_prompt += f"PID: {anomaly['pid']}, Name: {anomaly['name']}, CPU Usage: {anomaly.get('cpu_percent', 'N/A')}%, Memory Usage: {anomaly.get('memory_percent', 'N/A')}%\n"

    try:
        summary = ai_assistant.generate_explanation(summary_prompt)
    except Exception as e:
        st.write("An error occurred while generating the system security summary.")
        st.write(f"Error: {e}")
    st.subheader("System Security Summary")
    st.write(summary)

    # List anomalous processes
    st.subheader("Anomalous Processes")
    anomalies = neo4j_manager.run_query(
        "MATCH (p:Process) WHERE p.anomaly = true RETURN p.pid AS pid, p.name AS name, p.explanation AS explanation"
    )
    
    # Convert list of records to a DataFrame
    anomalies_data = [record for record in anomalies]
    # Remove duplicates
    seen_pids = set()
    unique_anomalies = []
    for record in anomalies_data:
        if record['pid'] not in seen_pids:
            seen_pids.add(record['pid'])
            unique_anomalies.append(record)

    for record in unique_anomalies:
        pid = record['pid']
        name = record['name']
        explanation = record.get('explanation', 'No explanation available.')

        st.write(f"**PID:** {pid} **Name:** {name}")
        st.write(f"**Explanation:** {explanation}")
        st.write("---")
        
    def display_security_analysis(neo4j_manager, ai_assistant):
        questions = [
            "What are the most critical vulnerabilities in the system? Which processes pose the highest risk?",
            # "what can you tell about the system? What is the primary purpose of the system? What are the key components of the system architecture? How does the system integrate with existing security infrastructure? What types of threats is the system designed to detect and mitigate? How does the system balance autonomy with human oversight? What types of data does the system collect? How is data collected from end-user devices and network infrastructure? What measures are in place to ensure data privacy and compliance with regulations? How is real-time data streaming and processing implemented? What data preprocessing techniques are employed?",
            # "What is the overall structure of the network I'm monitoring? How many endpoints, servers, and network devices are present? What are the primary communication patterns between different network segments? Are there any isolated or heavily secured network areas? What types of remote access methods are in use?", # Network Topology and Architecture
            # "What are the main data flows within the system? Are there any unexpected data transfers or communications? What protocols are predominantly used for internal and external communications? Are there any anomalies in data volume or frequency compared to baseline? Can I identify critical data paths that require extra monitoring?", # Data Flow Analysis
            # "What are the typical user activity patterns in different parts of the system? Are there users exhibiting behavior significantly different from their peers? Can I detect any potential insider threats based on unusual access patterns? What are the normal working hours, and are there justified reasons for off-hours access? Are there any sudden changes in individual user behavior that warrant investigation?", # User Behavior Patterns
            # "What are the baseline performance metrics for various system components? Are there any nodes consistently operating outside normal performance parameters? Can I correlate any performance anomalies with potential security issues? Are there any periodic patterns in system load or resource usage? How do system performance metrics change during known maintenance or update periods?", # System Performance Metrics
            # "What applications and services are running on the network? Are there any unauthorized or unexpected applications in use? What are the communication patterns of critical applications? Are all services and applications up-to-date with the latest security patches? Can I detect any applications exhibiting behavior consistent with malware?", # Application and Service Analysis
            # "What are the normal authentication patterns across the system? Are there any accounts showing multiple failed login attempts? Can I detect any unusual privilege escalation activities? Are there any unauthorized attempts to access restricted resources? What are the typical access patterns for different user roles, and are there deviations?", # Authentication and Access Patterns
            # "What are the normal patterns of communication with external networks? Are there any connections to known malicious IP addresses or domains? Can I detect any data exfiltration attempts? Are there any unusual spikes in outbound traffic? What are the typical destinations for outbound traffic, and are there any new ones?", # External Communication Analysis
            # "What known vulnerabilities exist in the system based on current configurations? Are there any critical vulnerabilities that require immediate attention? Can I correlate existing vulnerabilities with potential exploit attempts? What is the patch status across different system components? Are there any deprecated or end-of-life software versions still in use?", # Vulnerability Assessment
            # "What types of anomalies am I detecting most frequently? Are there patterns in the anomalies that suggest coordinated attacks? How do detected anomalies correlate with known threat intelligence? Are there any persistent low-level anomalies that might indicate long-term compromise? What is the false positive rate for different types of anomalies?", # Anomaly Detection
            # "How quickly are detected threats being addressed? What is the success rate of automated response actions? Are there recurring incidents that suggest ineffective mitigation strategies? How do incident response times vary across different types of threats? Are there any gaps in the current incident response procedures?", # Incident Response Efficacy
            # "What recent system changes or updates have occurred? How have these changes affected overall system behavior and security posture? Are there any unauthorized or unexpected system modifications? How do planned maintenance activities impact security metrics? Can I detect any attempts to alter system configurations maliciously?", #  System Updates and Changes
            # "What percentage of network traffic is encrypted? Are there any instances of sensitive data being transmitted unencrypted? Can I detect any attempts to bypass encryption mechanisms? Are encryption keys being managed and rotated according to best practices? Are there any weak encryption protocols still in use within the system?", # Data Encryption and Protection
            # "Are there any activities that violate established security policies? Can I detect any potential compliance issues based on data handling practices? Are there users or processes attempting to circumvent security controls? How effectively are data retention policies being enforced? Are there any unauthorized changes to critical system configurations?", # Compliance and Policy Adherence
            # "How do observed patterns correlate with known threat indicators? Are there any emerging threats that the system might be vulnerable to? Can I detect any activities matching recent threat intelligence reports?Are there any geographic or sector-specific threats relevant to this system? How rapidly is new threat intelligence being incorporated into detection mechanisms?", # Threat Intelligence Integration 
            # Add more questions...
        ]

        for question in questions:
            st.subheader(question)
            # Generate answer using AI Assistant
            answer = ai_assistant.generate_explanation(question)
            st.write(answer)
            
