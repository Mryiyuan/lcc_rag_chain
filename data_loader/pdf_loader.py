import os
from langchain_community.document_loaders import PyPDFLoader


def save_temp_file(uploaded_file):
    """Save uploaded file to a temporary location.
    
    Args:
        uploaded_file: The uploaded file object.
        
    Returns:
        str: Path to the temporary file.
    """
    temp_file_path = os.path.join("./temp", uploaded_file.name)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
    return temp_file_path


def remove_temp_file(temp_file_path):
    """Remove temporary file.
    
    Args:
        temp_file_path (str): Path to the temporary file.
    """
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)


def load_pdf_document(temp_file_path):
    """Load PDF document using PyPDFLoader.
    
    Args:
        temp_file_path (str): Path to the PDF file.
        
    Returns:
        list: List of document objects loaded from the PDF.
    """
    loader = PyPDFLoader(temp_file_path)
    return loader.load()