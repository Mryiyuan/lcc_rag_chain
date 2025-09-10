# RAG Chain - Generic Retrieval-Augmented Generation Application

[English](README.md) | [中文](README_CN.md)

RAG Chain is a Retrieval-Augmented Generation (RAG) application designed for general purpose document question answering. It allows users to ask questions about any topic and get accurate, context-aware answers based on uploaded documents.

## Features

- **Document Upload**: Upload PDF documents to enhance the knowledge base
- **RAG-based Q&A**: Ask questions about any topic and get context-aware answers
- **Modular Design**: Well-organized codebase with clear separation of concerns
- **Configurable Parameters**: Easily customize the application behavior through configuration
- **Streamlit UI**: User-friendly web interface for interaction

## Project Structure

```
rag_chain/
├── app.py                 # Original monolithic application (for reference)
├── main.py                # Application entry point with parameter support
├── config.py              # Configuration parameters
├── requirements.txt       # Python dependencies
├── data_loader/           # Module for loading documents
│   ├── __init__.py
│   └── pdf_loader.py      # PDF document loading functionality
├── text_splitter/         # Module for text splitting
│   ├── __init__.py
│   └── splitter.py        # Text splitting functionality
├── embedding/             # Module for embedding models
├── vector_db/             # Module for vector database operations
│   ├── __init__.py
│   ├── chroma_db.py       # Chroma database operations
│   └── add_documents.py   # Document addition functionality
├── rag_chain/             # Module for RAG chain operations
│   ├── __init__.py
│   └── chain.py           # RAG chain implementation
├── ui/                    # Module for user interface
│   ├── __init__.py
│   └── interface.py       # Streamlit UI implementation
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── helpers.py         # Helper functions
├── temp/                  # Temporary files directory
├── chroma_db/             # Chroma database files
└── docker-compose/        # Docker Compose configurations
    ├── Qwen3-0.6B-GPTQ-Int8/  # Qwen3 LLM model Docker configuration
    └── Qwen3-Embedding-0.6B/  # Qwen3 Embedding model Docker configuration
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Mryiyuan/lcc_rag_chain.git
   cd lcc_rag_chain
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application can be configured through the `config.py` file or command-line arguments:

### Configuration Parameters

- `EMBEDDING_API_BASE`: Embedding model API base URL
- `VLLM_API_BASE`: vLLM API base URL
- `CHUNK_SIZE`: Text chunk size for document splitting
- `CHUNK_OVERLAP`: Text chunk overlap for document splitting
- `SEARCH_K`: Number of documents to retrieve in similarity search
- `MAX_TOKENS`: Maximum tokens for LLM response
- `TEMPERATURE`: Temperature for LLM response generation

### Command-Line Arguments

- `--host`: Host address to run the application on (default: localhost)
- `--port`: Port number to run the application on (default: 8501)
- `--embedding-api-base`: Embedding API base URL
- `--vllm-api-base`: vLLM API base URL
- `--chunk-size`: Text chunk size for document splitting
- `--chunk-overlap`: Text chunk overlap for document splitting
- `--search-k`: Number of documents to retrieve in similarity search

## Usage

1. Start the application:
   ```bash
   streamlit run main.py
   ```

2. Or start with custom parameters:
   ```bash
   streamlit run main.py --port 8502 --chunk-size 1024
   ```

3. Open your browser and navigate to `http://localhost:8501` (or your custom port)

4. Use the interface to:
   - Ask questions in the main text area
   - Upload PDF documents in the sidebar
   - View model configuration information

## Modules Description

### Data Loader (`data_loader/`)
Handles loading of PDF documents:
- `save_temp_file()`: Saves uploaded files to temporary location
- `remove_temp_file()`: Removes temporary files after processing
- `load_pdf_document()`: Loads PDF documents using PyPDFLoader

### Text Splitter (`text_splitter/`)
Handles text splitting of documents:
- `create_recursive_splitter()`: Creates a RecursiveCharacterTextSplitter
- `split_documents()`: Splits documents into smaller chunks

### Vector Database (`vector_db/`)
Handles vector database operations:
- `add_documents_to_db()`: Adds documents to the Chroma database
- `get_retriever()`: Gets a retriever object for similarity search
- `add_to_db()`: Processes and adds uploaded files to the database

### RAG Chain (`rag_chain/`)
Implements the Retrieval-Augmented Generation chain:
- `run_rag_chain()`: Processes queries using RAG chain

### UI (`ui/`)
Implements the Streamlit user interface:
- `render_main_page()`: Renders the main application page
- `render_sidebar()`: Renders the sidebar with configuration and file upload

### Utilities (`utils/`)
Contains helper functions:
- `format_docs()`: Formats document objects into a single string

## Requirements

- Python 3.8+
- Streamlit
- Langchain
- ChromaDB
- OpenAI Python SDK
- PyPDF2

See `requirements.txt` for detailed dependencies.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.# rag_chain

## Docker Deployment

The `docker-compose` directory contains configurations for running the Qwen3 models as Docker containers. This provides a convenient way to deploy the required model services.

### Prerequisites
- Docker and Docker Compose installed on your system
- NVIDIA GPU with CUDA support (for GPU acceleration)
- NVIDIA Container Toolkit installed

### Available Configurations

1. **Qwen3-0.6B-GPTQ-Int8**: Configuration for running the Qwen3 language model with GPTQ quantization
2. **Qwen3-Embedding-0.6B**: Configuration for running the Qwen3 embedding model

### Usage

1. First, ensure you have the Qwen3 models available locally. The default configuration assumes the models are located at:
   - Qwen3-0.6B-GPTQ-Int8: `D:\model\Qwen3-0.6B-GPTQ-Int8`
   - Qwen3-Embedding-0.6B: `D:/model/Qwen/Qwen3-Embedding-0.6B`

   **Note**: If your models are located in a different directory, you need to update the volume mappings in the respective `docker-compose.yml` files.

2. Start the desired service:

   For the language model:
   ```bash
   cd docker-compose/Qwen3-0.6B-GPTQ-Int8
   docker-compose up -d
   ```

   For the embedding model:
   ```bash
   cd docker-compose/Qwen3-Embedding-0.6B
   docker-compose up -d
   ```

3. Verify that the services are running:
   ```bash
   docker-compose ps
   ```

4. Update the application configuration (`config.py` or via command-line arguments) to point to these services:
   - LLM service: `http://localhost:8800/v1`
   - Embedding service: `http://localhost:50001/v1`

### Configuration Notes
- Both configurations use the `vllm/vllm-openai:v0.10.1.1` image
- API keys are set to default values (`sk-123456` and `sk123456`) for testing purposes
- GPU memory utilization and other parameters are optimized for typical usage scenarios
- The embedding service uses the `pooling` runner to generate embeddings
