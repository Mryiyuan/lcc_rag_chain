from config import db, Config


def add_documents_to_db(documents):
    """Add documents to the vector database.
    
    Args:
        documents (list): List of document chunks to add to the database.
    """
    db.add_documents(documents)


def get_retriever():
    """Get a retriever object for similarity search.
    
    Returns:
        Retriever: A retriever object configured for similarity search.
    """
    return db.as_retriever(search_type="similarity", search_kwargs={'k': Config.SEARCH_K})


def delete_documents_by_file_id(file_id):
    """Delete documents from the vector database based on file_id.
    
    Args:
        file_id (str): The unique identifier of the file to delete documents for.
    
    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        # Get all documents with the specified file_id
        all_docs = db.get()
        ids_to_delete = []
        
        # Check if 'metadatas' exists and has entries
        if 'metadatas' in all_docs and all_docs['metadatas']:
            for i, metadata in enumerate(all_docs['metadatas']):
                if metadata and "file_id" in metadata and metadata["file_id"] == file_id:
                    if 'ids' in all_docs and i < len(all_docs['ids']):
                        ids_to_delete.append(all_docs['ids'][i])
        
        # Delete the matched documents
        if ids_to_delete:
            db.delete(ids=ids_to_delete)
            return True
        return False
    except Exception as e:
        print(f"Error deleting documents: {e}")
        return False