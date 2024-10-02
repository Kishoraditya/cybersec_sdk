# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

#ARG NEO4J_URI
#ARG NEO4J_USER
#ARG NEO4J_PASSWORD
# Set environment variables for Neo4j connection
#ENV NEO4J_URI=bolt://neo4j:7687
ENV NEO4J_URI = $(NEO4J_URI)
ENV NEO4J_USER = ${NEO4J_USER}
ENV NEO4J_PASSWORD = ${NEO4J_PASSWORD}
# docker run --env-file .env cyberguard
# NEO4J_PASSWORD will be provided at runtime

# Run the application
CMD ["streamlit", "run", "ui.py", "--server.address=0.0.0.0"]
