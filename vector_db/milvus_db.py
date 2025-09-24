import logging
from pymilvus import FieldSchema, CollectionSchema, DataType
from config import db, Config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def add_documents_to_db(documents):
    """Add documents to the Milvus vector database.
    
    Args:
        documents (list): List of document chunks to add to the database.
    
    Returns:
        str: Status message indicating success or failure.
    """
    try:
        # For Milvus, we need to use the underlying client for some operations
        from config import client
        
        # Check if collection exists
        if not client.has_collection(Config.MILVUS_COLLECTION_NAME):
            logger.warning(f"Collection {Config.MILVUS_COLLECTION_NAME} does not exist")
            
            # Define collection schema
            from pymilvus import FieldSchema, CollectionSchema, DataType
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
                FieldSchema(name="file_name", dtype=DataType.VARCHAR, max_length=255)
            ]
            
            schema = CollectionSchema(fields=fields, description="RAG collection")
            
            # Create collection
            client.create_collection(
                collection_name=Config.MILVUS_COLLECTION_NAME,
                schema=schema
            )
            
            logger.info(f"Created collection {Config.MILVUS_COLLECTION_NAME}")
        
        # Add documents to the database using the LangChain Milvus instance
        db.add_documents(documents)
        logger.info(f"Added {len(documents)} documents to the database.")
        return f"Added {len(documents)} documents to the database."
    except Exception as e:
        logger.error(f"Error adding documents: {str(e)}")
        return f"Error adding documents: {str(e)}"


def get_retriever():
    """Get a retriever from the Milvus vector database.
    
    Returns:
        object: A retriever object that can be used for similarity search.
    """
    try:
        # Create a retriever from the database
        retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": Config.SEARCH_K}
        )
        logger.info(f"Created retriever with top_k={Config.SEARCH_K}")
        return retriever
    except Exception as e:
        logger.error(f"Error creating retriever: {str(e)}")
        raise


def delete_documents_by_file_id(file_id):
    """Delete documents from the vector database based on file_id.
    
    Args:
        file_id (str): The unique identifier of the file to delete documents for.
    
    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        # For Milvus, we need to use the underlying client for metadata-based deletion
        from config import client
        
        # Check if collection exists
        if not client.has_collection(Config.MILVUS_COLLECTION_NAME):
            logger.warning(f"Collection {Config.MILVUS_COLLECTION_NAME} does not exist")
            return False
        
        # Search for documents with the specified file_id
        # In Milvus, we need to use a query to find documents by metadata
        expr = f"file_name == '{file_id}'"
        results = client.query(
            collection_name=Config.MILVUS_COLLECTION_NAME,
            expr=expr,
            output_fields=["id"]
        )
        
        if not results:
            logger.info(f"No documents found with file_id: {file_id}")
            return False
        
        # Extract the IDs to delete
        ids_to_delete = [result["id"] for result in results]
        
        # Delete the matched documents
        client.delete(
            collection_name=Config.MILVUS_COLLECTION_NAME,
            ids=ids_to_delete
        )
        
        logger.info(f"Successfully deleted {len(ids_to_delete)} documents with file_id: {file_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting documents: {str(e)}")
        return False