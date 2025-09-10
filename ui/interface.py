import sys
import os

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from rag_chain.chain import run_rag_chain_stream
from vector_db.add_documents import add_to_db
from vector_db.chroma_db import delete_documents_by_file_id
from config import Config

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize uploaded files list
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []


def render_main_page():
    """Render the main page of the application with chat interface."""
    st.set_page_config(page_title="Retrieval System", page_icon=":microscope:")
    st.title("Retrieval System")
    st.subheader("Chat with your knowledge base")

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    # Chat input box
    if prompt := st.chat_input("Ask a question"):
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Create placeholder for streaming output
                message_placeholder = st.empty()
                full_response = ""
                
                # Get streaming response with chat history
                for chunk in run_rag_chain_stream(query=prompt, chat_history=st.session_state.chat_history):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                # Display final response
                message_placeholder.markdown(full_response)
                
                # Add assistant response to history
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})


def render_sidebar():
    """Render the sidebar of the Retrieval System application."""
    with st.sidebar:
        st.title("Model Configuration")
        st.info("Using local vLLM with Qwen3-0.6B model")
        # st.write(f"Base URL: {Config.VLLM_API_BASE}")
        st.write(f"Model: {Config.VLLM_MODEL_NAME}")
        
        # Add no-thought mode toggle
        no_thought_mode = st.toggle("Enable No-Thought Mode", value=Config.NO_THINK_MODE)
        if no_thought_mode != Config.NO_THINK_MODE:
            Config.NO_THINK_MODE = no_thought_mode
            st.success(f"No-Thought Mode {'enabled' if no_thought_mode else 'disabled'}")
        
        # Chat history management
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
    
    with st.sidebar:
        st.markdown("---")
        pdf_docs = st.file_uploader("Upload your research documents :memo:",
                                    type=["pdf"],
                                    accept_multiple_files=True
        )
        
        if st.button("Submit & Process"):
            if not pdf_docs:
                st.warning("Please upload the file")
            else:
                with st.spinner("Processing your documents..."):
                    add_to_db(pdf_docs)
                    st.success(":file_folder: Documents successfully added to the database!")
        
        # Uploaded files management
        st.markdown("---")
        st.subheader("Uploaded Files")
        
        # Helper function to format file size
        def format_size(size_bytes):
            """Format byte size into human-readable format"""
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1048576:
                return f"{size_bytes/1024:.2f} KB"
            else:
                return f"{size_bytes/1048576:.2f} MB"
        
        # Display uploaded files with delete option
        if st.session_state.uploaded_files:
            for file in st.session_state.uploaded_files:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{file['name']}**")
                    st.caption(f"Size: {format_size(file['size'])}")
                    st.caption(f"Upload time: {file['upload_time']}")
                with col2:
                    if st.button("Delete", key=f"delete_{file['id']}"):
                        # Delete documents from vector database
                        success = delete_documents_by_file_id(file['id'])
                        if success:
                            # Remove file from session state
                            st.session_state.uploaded_files = [
                                f for f in st.session_state.uploaded_files if f['id'] != file['id']
                            ]
                            st.success(f"Successfully deleted '{file['name']}' and its vectors")
                            # Refresh page to update list
                            st.rerun()
                        else:
                            st.error(f"Failed to delete vectors for '{file['name']}'")
        else:
            st.info("No files uploaded yet.")
        
        # Sidebar footer
        st.write("Built with ❤️ by [LiChenchen]()")