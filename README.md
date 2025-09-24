# RAG Chain - Generic Retrieval-Augmented Generation Application

[English](README.md) | [中文](README_CN.md)

RAG Chain is a Retrieval-Augmented Generation (RAG) application designed for general purpose document question answering. It allows users to ask questions about any topic and get accurate, context-aware answers based on uploaded documents.

## Features

- **Document Upload**: Upload PDF documents to enhance the knowledge base
- **RAG-based Q&A**: Ask questions about any topic and get context-aware answers
- **Modular Design**: Well-organized codebase with clear separation of concerns
- **Configurable Parameters**: Easily customize the application behavior through configuration
- **Streamlit UI**: User-friendly web interface for interaction
- **Milvus Vector Database**: High-performance, scalable vector search engine for efficient document retrieval
- **Docker Deployment**: One-click containerization, memory-efficient deployment
  - All models (LLM/embedding/reranker) built on [vllm/vllm-openai](https://hub.docker.com/r/vllm/vllm-openai) official image with automatic tensor-parallelism for minimal GPU memory usage
  - Local testing: `docker compose up -d` to start the complete service; For production, simply modify model names in `.env` or update `OPENAI_BASE_URL` to instantly switch to any OpenAI-compatible model (GPT, Claude, Qwen, Baichuan, etc.)
  - Provides `Dockerfile` & `docker-compose.yml`, supporting both CPU debugging and GPU inference modes, zero changes needed for cloud deployment

## Project Structure

```
lcc_rag_chain/
├── .gitignore             # Git ignore file
├── LICENSE                # License file
├── README.md              # English documentation
├── README_CN.md           # Chinese documentation
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
│   ├── __init__.py
│   └── embedder.py        # Embedding model implementation
├── vector_db/             # Module for vector database operations
│   ├── __init__.py
│   ├── milvus_db.py       # Milvus database operations
│   └── add_documents.py   # Document addition functionality
├── rag_chain/             # Module for RAG chain operations
│   ├── __init__.py
│   └── chain.py           # RAG chain implementation
├── ui/                    # Module for user interface
│   ├── __init__.py
│   └── interface.py       # Streamlit UI implementation
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── helpers.py         # Helper functions
│   └── reranker.py        # Document reranker implementation
├── temp/                  # Temporary files directory
├── test_milvus.py         # Comprehensive Milvus test script
├── test_milvus_connection.py # Milvus connection test
├── test_milvus_simple.py  # Simplified Milvus test script
└── docker-compose/        # Docker Compose configurations
    ├── Qwen3-0.6B-GPTQ-Int8/  # Qwen3 LLM model Docker configuration
    ├── Qwen3-Embedding-0.6B/  # Qwen3 Embedding model Docker configuration
    └── Qwen3-Reranker-0.6B/   # Qwen3 Reranker model Docker configuration
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
- `EMBEDDING_API_KEY`: API key for the embedding service
- `EMBEDDING_MODEL_NAME`: Name of the embedding model
- `VLLM_API_BASE`: vLLM API base URL
- `CHUNK_SIZE`: Text chunk size for document splitting
- `CHUNK_OVERLAP`: Text chunk overlap for document splitting
- `SEARCH_K`: Number of documents to retrieve in similarity search
- `MAX_TOKENS`: Maximum tokens for LLM response
- `TEMPERATURE`: Temperature for LLM response generation
- `MILVUS_URI`: Milvus server connection URI
- `MILVUS_TOKEN`: Milvus authentication token
- `MILVUS_DATABASE`: Milvus database name
- `MILVUS_COLLECTION_NAME`: Milvus collection name
- `MILVUS_TIMEOUT`: Milvus connection timeout (in seconds)

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
   streamlit run main.py --server.port 8502
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
Handles vector database operations using Milvus:
- `add_documents_to_db()`: Adds documents to the Milvus database
- `get_retriever()`: Gets a retriever object for similarity search
- `add_to_db()`: Processes and adds uploaded files to the database
- `delete_documents_by_file_id()`: Deletes documents from the database based on file identifier

### RAG Chain (`rag_chain/`)
Implements the Retrieval-Augmented Generation chain:
- `run_rag_chain()`: Processes queries using RAG chain with document retrieval and LLM generation
- `get_prompt_template()`: Creates prompt templates for LLM interactions

### UI (`ui/`)
Implements the Streamlit user interface:
- `render_main_page()`: Renders the main application page
- `render_sidebar()`: Renders the sidebar with configuration and file upload
- `clear_messages()`: Clears chat history

### Embedding (`embedding/`)
Handles text embedding functionality:
- `get_embedding_model()`: Returns the configured embedding model instance

### Utilities (`utils/`)
Contains helper functions:
- `format_docs()`: Formats document objects into a single string
- `get_reranker()`: Returns a reranker model for improving search results

### Test Scripts
The project includes several test scripts for verifying Milvus database functionality:
- `test_milvus_simple.py`: Simplified test for Milvus connection and basic operations
- `test_milvus_connection.py`: Tests Milvus connection and configuration
- `test_milvus.py`: Comprehensive test for Milvus database operations

### Running the Tests
To verify that Milvus is configured correctly and functioning properly, you can run the test scripts:

```bash
# Run the simplified Milvus test
python test_milvus_simple.py

# Run the Milvus connection test
python test_milvus_connection.py

# Run the comprehensive Milvus test
python test_milvus.py
```

These tests will verify:
- Milvus server connection
- Embedding model functionality
- Document addition to Milvus
- Document retrieval and search
- Document deletion

## Requirements

- Python 3.8+
- Streamlit
- Langchain
- Langchain Milvus
- PyMilvus
- OpenAI Python SDK
- PyPDF
- sentence-transformers
- loguru

See `requirements.txt` for detailed dependencies.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Docker Deployment

The `docker-compose` directory contains configurations for running the Qwen3 models as Docker containers. This provides a convenient way to deploy the required model services.

### Prerequisites
- Docker and Docker Compose installed on your system
- NVIDIA GPU with CUDA support (for GPU acceleration)
- NVIDIA Container Toolkit installed

### Available Configurations

1. **Qwen3-0.6B-GPTQ-Int8**: Configuration for running the Qwen3 language model with GPTQ quantization
2. **Qwen3-Embedding-0.6B**: Configuration for running the Qwen3 embedding model
3. **Qwen3-Reranker-0.6B**: Configuration for running the Qwen3 reranker model

### Usage

1. First, ensure you have the Qwen3 models available locally. The default configuration assumes the models are located at:
   - Qwen3-0.6B-GPTQ-Int8: `D:\model\Qwen3-0.6B-GPTQ-Int8`
   - Qwen3-Embedding-0.6B: `D:/model/Qwen/Qwen3-Embedding-0.6B`
   - Qwen3-Reranker-0.6B: `D:/model/Qwen/Qwen3-Reranker-0.6B`

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

   For the reranker model:
   ```bash
   cd docker-compose/Qwen3-Reranker-0.6B
   docker-compose up -d
   ```

3. Verify that the services are running:
   ```bash
   docker-compose ps
   ```

4. Update the application configuration (`config.py` or via command-line arguments) to point to these services:
   - LLM service: `http://localhost:8800/v1`
   - Embedding service: `http://localhost:50001/v1`
   - Reranker service: `http://localhost:60001/v1`

### Configuration Notes
- All configurations use the `vllm/vllm-openai:v0.10.1.1` image
- API keys are set to default values (`sk-123456`, `sk123456`) for testing purposes
- GPU memory utilization and other parameters are optimized for typical usage scenarios
- The embedding service uses the `pooling` runner to generate embedding vectors
