# test_neo4j_connection.py

from neo4j import GraphDatabase
from neo4j.exceptions import AuthError, ServiceUnavailable

uri = "bolt://localhost:7687"
user = "neo4j"
password = "Qwerty@123"

def test_connection():
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run("RETURN 1 AS number")
            record = result.single()
            print(f"Connection successful, received: {record['number']}")
        driver.close()
    except AuthError as e:
        print(f"Authentication failed: {e}")
    except ServiceUnavailable as e:
        print(f"Service unavailable: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_connection()
