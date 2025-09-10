import streamlit as st
import uuid
import datetime
from data_loader.pdf_loader import save_temp_file, remove_temp_file, load_pdf_document
from text_splitter.splitter import create_recursive_splitter, split_documents
from config import db


def add_to_db(uploaded_files):
    """Processes and adds uploaded PDF files to the database.

    This function checks if any files have been uploaded. If files are uploaded,
    it saves each file to a temporary location, processes the content using a PDF loader,
    and splits the content into smaller chunks. Each chunk, along with its metadata, 
    is then added to the database. Temporary files are removed after processing.

    Args:
        uploaded_files (list): A list of uploaded file objects to be processed.

    Returns:
        None"""
    # Check if files are uploaded
    if not uploaded_files:
        # In modular version, we'll let the UI handle error messaging
        return

    # Initialize uploaded_files list in session state if not exists
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

    for uploaded_file in uploaded_files:
        # Generate unique ID for the file
        file_id = str(uuid.uuid4())
        file_name = uploaded_file.name
        upload_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_size = uploaded_file.size

        # Save the uploaded file to a temporary path
        temp_file_path = save_temp_file(uploaded_file)

        # Load the file using PyPDFLoader
        documents = load_pdf_document(temp_file_path)

        # Create text splitter and split documents
        splitter = create_recursive_splitter()
        doc_chunks = split_documents(splitter, documents)

        # Add file metadata to each chunk for later retrieval and deletion
        for chunk in doc_chunks:
            chunk.metadata["file_id"] = file_id
            chunk.metadata["file_name"] = file_name
            chunk.metadata["upload_time"] = upload_time

        # Add chunks to database
        db.add_documents(doc_chunks)

        # Remove the temporary file after processing
        remove_temp_file(temp_file_path)

        # Add file information to session state
        st.session_state.uploaded_files.append({
            "id": file_id,
            "name": file_name,
            "size": file_size,
            "upload_time": upload_time
        })