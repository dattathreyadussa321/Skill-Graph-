import os
import logging
from dotenv import load_dotenv
from py2neo import Graph
from neomodel import db

load_dotenv()

logger = logging.getLogger(__name__)

# Lazy connection holders
_graph = None
_neomodel_configured = False


def _get_neo4j_config():
    """Get Neo4j connection config from environment variables."""
    scheme = os.getenv('SCHEME', 'bolt://')
    url = os.getenv('URL', 'localhost:7687')
    username = os.getenv('NEO4J_USER', os.getenv('USERNAMEE', 'neo4j'))
    password = os.getenv('PASSWORD', 'neo4jpass')
    return scheme, url, username, password


def get_graph():
    """Get a lazy py2neo Graph connection using .env variables."""
    global _graph
    if _graph is None:
        scheme, url, username, password = _get_neo4j_config()
        connection_url = f"{scheme}{url}"
        try:
            _graph = Graph(connection_url, auth=(username, password))
            logger.info(f"Connected to Neo4j at {connection_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j at {connection_url}: {e}")
            raise
    return _graph


def reset_graph():
    """Reset the graph connection (useful after connection errors)."""
    global _graph
    _graph = None


def configure_neomodel():
    """Configure neomodel database connection using .env variables."""
    global _neomodel_configured
    if not _neomodel_configured:
        _, url, username, password = _get_neo4j_config()
        connection_url = f'bolt://{username}:{password}@{url}'
        db.set_connection(connection_url)
        _neomodel_configured = True
        logger.info("Neomodel configured successfully")


def check_connection():
    """Test the Neo4j connection and return status."""
    try:
        graph = get_graph()
        result = graph.run("RETURN 1 AS test").data()
        if result and result[0]['test'] == 1:
            return {"status": "connected", "message": "Neo4j connection successful"}
        return {"status": "error", "message": "Unexpected response from Neo4j"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
