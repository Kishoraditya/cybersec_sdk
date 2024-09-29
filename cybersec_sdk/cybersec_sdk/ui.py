# cybersec_sdk/ui.py

import streamlit as st
from neo4j import GraphDatabase

def run_ui(neo4j_manager):
    st.title("Cybersecurity SDK Dashboard")

    # Display summary statistics
    processes = neo4j_manager.run_query("MATCH (p:Process) RETURN count(p) AS process_count")
    users = neo4j_manager.run_query("MATCH (u:User) RETURN count(u) AS user_count")
    anomalies = neo4j_manager.run_query("MATCH (p:Process) WHERE p.anomaly = true RETURN count(p) AS anomaly_count")

    st.metric("Total Processes", processes[0]['process_count'])
    st.metric("Total Users", users[0]['user_count'])
    st.metric("Anomalous Processes", anomalies[0]['anomaly_count'])

    # List anomalous processes
    st.subheader("Anomalous Processes")
    anomaly_results = neo4j_manager.run_query("MATCH (p:Process) WHERE p.anomaly = true RETURN p.id AS pid, p.name AS name, p.explanation AS explanation")
    for record in anomaly_results:
        st.write(f"**PID:** {record['pid']} **Name:** {record['name']}")
        st.write(f"**Explanation:** {record.get('explanation', 'No explanation available.')}")
        st.write("---")
