
# **architecture.md**

## **System Architecture Overview**

### **Components:**

1. **Data Collection Layer:**

   - **SystemAnalyzer (`analyzer.py`):**
     - Collects data from the host system using `psutil`.
     - Gathers information on processes, network connections, users, etc.

2. **Data Storage Layer:**

   - **Neo4j Graph Database:**
     - Stores nodes and relationships representing system entities.
     - Allows for complex queries and relationship mapping.

   - **Neo4jManager (`neo4j_manager.py`):**
     - Facilitates communication between the application and the Neo4j database.
     - Provides methods to create nodes, relationships, and run queries.

3. **Data Processing Layer:**

   - **GraphManager (`graph_manager.py`):**
     - Manages the construction of the graph structure.
     - Sanitizes data and builds relationships between nodes.

   - **AnomalyDetector (`ml_models.py`):**
     - Applies machine learning algorithms to detect anomalies.
     - Uses Isolation Forest for unsupervised anomaly detection.

4. **Intelligence Layer:**

   - **AIAssistant (`ai_assistant.py`):**
     - Generates natural language explanations for detected anomalies.
     - Integrates with the Gemini AI API.

5. **Presentation Layer:**

   - **Dashboard (`ui.py`):**
     - Provides an interactive user interface using Streamlit.
     - Displays metrics, anomalies, and detailed explanations.

6. **External Data Integration:**

   - **ThreatIntelFeed (`external_data.py`):**
     - Retrieves and integrates external threat intelligence data.

### **Data Flow:**

1. **Data Collection:**
   - `SystemAnalyzer` collects system data.

2. **Data Storage:**
   - `GraphManager` adds data to Neo4j via `Neo4jManager`.

3. **Anomaly Detection:**
   - Data is converted into a DataFrame for processing.
   - `AnomalyDetector` identifies anomalies.

4. **AI Explanation:**
   - `AIAssistant` generates explanations for anomalies.

5. **Visualization:**
   - `run_ui` displays data on the Streamlit dashboard.

### **Inter-Module Interactions:**

- `example_usage.py` orchestrates the interaction between modules.
- `GraphManager` relies on `Neo4jManager` for database operations.
- `AnomalyDetector` processes data collected by `SystemAnalyzer`.
- `AIAssistant` uses results from `AnomalyDetector` to generate explanations.

### **Technologies Used:**

- **Python Libraries:**
  - `psutil` for system data.
  - `pandas` and `numpy` for data manipulation.
  - `scikit-learn` for machine learning.
  - `streamlit` for the UI.
- **Databases:**
  - Neo4j for graph data storage.
- **APIs:**
  - Gemini AI API for natural language processing.

---

## **Deployment Considerations**

- **Scalability:**
  - Neo4j can handle large datasets, but performance tuning may be required.
- **Security:**
  - Secure API keys and database credentials.
  - Ensure proper user authentication for the dashboard.
- **Extensibility:**
  - Modular design allows for easy addition of new features or data sources.

---
