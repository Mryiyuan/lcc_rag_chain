import sys
import sys
import argparse
from ui.interface import render_main_page, render_sidebar
from config import Config


def main(host="localhost", port=8501):
    """Initialize and manage the PharmaQuery application interface.

    This function sets up the Streamlit application interface for PharmaQuery,
    a Pharmaceutical Insight Retrieval System. Users can enter queries related
    to the pharmaceutical industry, upload research documents, and manage API 
    keys for enhanced functionality.

    The main features include:
    - Query input area for users to ask questions about the pharmaceutical industry.
    - Submission button to process the query and display the retrieved insights.
    - Sidebar for API key input and management.
    - File uploader for adding research documents to the database, enhancing query responses.

    Args:
        host (str): Host address to run the application on.
        port (int): Port number to run the application on.

    Returns:
        None"""
    render_main_page()
    render_sidebar()


if __name__ == "__main__":
    # Check if we're running in Streamlit
    if "streamlit" in sys.modules or any("streamlit" in arg for arg in sys.argv):
        main()
    else:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description="PharmaQuery - Pharmaceutical Insight Retrieval System")
        parser.add_argument("--host", type=str, default="localhost", help="Host address to run the application on")
        parser.add_argument("--port", type=int, default=8501, help="Port number to run the application on")
        parser.add_argument("--embedding-api-base", type=str, help="Embedding API base URL")
        parser.add_argument("--vllm-api-base", type=str, help="vLLM API base URL")
        parser.add_argument("--chunk-size", type=int, help="Text chunk size for document splitting")
        parser.add_argument("--chunk-overlap", type=int, help="Text chunk overlap for document splitting")
        parser.add_argument("--search-k", type=int, help="Number of documents to retrieve in similarity search")
        parser.add_argument("--no-think", action="store_true", help="Enable no-think mode to remove thought blocks from responses")
        
        args = parser.parse_args()
        
        # Update config with command line arguments if provided
        if args.embedding_api_base:
            Config.EMBEDDING_API_BASE = args.embedding_api_base
        if args.vllm_api_base:
            Config.VLLM_API_BASE = args.vllm_api_base
        if args.chunk_size:
            Config.CHUNK_SIZE = args.chunk_size
        if args.chunk_overlap:
            Config.CHUNK_OVERLAP = args.chunk_overlap
        if args.search_k:
            Config.SEARCH_K = args.search_k
        if args.no_think:
            Config.NO_THINK_MODE = True
            
        # Run the Streamlit app
        import streamlit.web.bootstrap
        streamlit.web.bootstrap.run(__file__, command_line=None, args=[f"--server.port={args.port}", f"--server.address={args.host}"])