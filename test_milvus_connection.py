import logging
from pymilvus import MilvusClient
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_milvus_connection():
    """Test connection to Milvus server and verify database and collection exist."""
    try:
        logger.info(f"Attempting to connect to Milvus at {Config.MILVUS_URI}")
        
        # Create Milvus client
        client = MilvusClient(
            uri=Config.MILVUS_URI,
            token=Config.MILVUS_TOKEN,
            timeout=Config.MILVUS_TIMEOUT
        )
        
        logger.info("Successfully connected to Milvus server")
        
        # List all databases
        databases = client.list_databases()
        logger.info(f"Available databases: {[db['name'] for db in databases]}")
        
        # Switch to the target database
        client.using_database(Config.MILVUS_DATABASE)
        logger.info(f"Switched to database: {Config.MILVUS_DATABASE}")
        
        # Check if collection exists
        collections = client.list_collections()
        logger.info(f"Available collections in {Config.MILVUS_DATABASE}: {collections}")
        
        if Config.MILVUS_COLLECTION_NAME in collections:
            logger.info(f"Collection {Config.MILVUS_COLLECTION_NAME} exists")
            
            # Get collection statistics
            stats = client.get_collection_stats(Config.MILVUS_COLLECTION_NAME)
            logger.info(f"Collection statistics: {stats}")
        else:
            logger.warning(f"Collection {Config.MILVUS_COLLECTION_NAME} does not exist yet")
            logger.info(f"It will be created automatically when adding documents")
        
        logger.info("Milvus connection test completed successfully")
        return True
    except Exception as e:
        logger.error(f"Milvus connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_milvus_connection()