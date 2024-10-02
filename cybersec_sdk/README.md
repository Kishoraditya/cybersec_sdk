# **README.md**

## **Cybersecurity Monitoring SDK**

### **Overview**

The Cybersecurity Monitoring SDK is a Python-based tool designed to analyze system processes, detect anomalies, and visualize data through a user-friendly dashboard. It leverages system monitoring libraries, a graph database, machine learning models, and AI-powered explanations to provide insights into your system's security posture.

### **Features**

- **System Analysis:**
  - Collects data on running processes, network connections, users, and open files.
- **Anomaly Detection:**
  - Uses Isolation Forest algorithm to identify anomalous processes based on resource usage.
- **Graph Database Integration:**
  - Stores and manages data using Neo4j for efficient querying and relationship mapping.
- **AI Assistant:**
  - Generates explanations for anomalies using the Gemini AI API.
- **Interactive Dashboard:**
  - Visualizes data and anomalies using Streamlit for easy monitoring.

### **Prerequisites**

- Python 3.7 or higher
- Neo4j Graph Database
- Gemini AI API Key (from Google AI Studio)

### **Installation**

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/kishoraditya/cybersec_sdk.git
   cd cybersec_sdk
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Neo4j:**

   - Download and install Neo4j Desktop or Community Edition.
   - Start the Neo4j server and set your username and password.

4. **Configure Environment Variables:**

   ```bash
   export NEO4J_URI=bolt://localhost:7687
   export NEO4J_USER=neo4j
   export NEO4J_PASSWORD=your_neo4j_password
   export API_KEY=your_gemini_api_key
   ```

### **Usage**

1. **Run the Main Script:**

   ```bash
   python example_usage.py
   ```

2. **Launch the Dashboard:**

   If not automatically opened, run:

   ```bash
   streamlit run example_usage.py
   ```

3. **Explore the Dashboard:**

   - Access the dashboard at `http://localhost:8501`.
   - View total processes, users, and anomalous processes.
   - Examine detailed explanations for each anomaly.

### **Customization**

- **Adjust Anomaly Detection:**
  - Modify `ml_models.py` to fine-tune the Isolation Forest parameters.
- **Update Data Collection:**
  - Edit `analyzer.py` to collect additional system metrics.
- **Enhance the Dashboard:**
  - Customize `ui.py` to improve the user interface and add new features.

### **Contributing**

Contributions are welcome! Please submit a pull request or open an issue to discuss changes.

### **License**

Refer to the LICENSE file

---
