from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import Config


def create_recursive_splitter():
    """Create a RecursiveCharacterTextSplitter with predefined settings.
    
    Returns:
        RecursiveCharacterTextSplitter: Configured text splitter.
    """
    return RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", ". ", " ", ""],
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        length_function=len,
    )


def split_documents(splitter, documents):
    """Split documents into smaller chunks.
    
    Args:
        splitter: The text splitter to use.
        documents (list): List of document objects to split.
        
    Returns:
        list: List of document chunks.
    """
    doc_content = [doc.page_content for doc in documents]
    doc_metadata = [doc.metadata for doc in documents]
    return splitter.create_documents(doc_content, doc_metadata)