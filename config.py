import os
from pymilvus import MilvusClient, FieldSchema, CollectionSchema, DataType
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings.base import Embeddings
from langchain_milvus import Milvus

# Configuration parameters
class Config:
    # API Configuration
    EMBEDDING_API_BASE = "http://host.docker.internal:50001/v1"
    EMBEDDING_API_KEY = "sk123456"
    EMBEDDING_MODEL_NAME = "qwen3-ebd-0d6"
    
    # vLLM Configuration
    VLLM_API_BASE = "http://host.docker.internal:8800/v1"
    VLLM_API_KEY = "sk-123456"
    VLLM_MODEL_NAME = "Qwen3-0.6B-GPTQ-Int8"
    
    # Rerank Configuration
    RERANK_ENABLED = True
    RERANK_API_BASE = "http://host.docker.internal:60001/v1"
    RERANK_API_KEY = "sk123456"
    RERANK_MODEL_NAME = "qwen3-reranker-0d6"
    RERANK_TOP_K = 3  # Number of documents to keep after reranking
    
    # Database Configuration
    MILVUS_URI = "http://192.168.50.3:19530"
    MILVUS_TOKEN = "root:Milvus"
    MILVUS_DATABASE = "rag_db"
    MILVUS_COLLECTION_NAME = "pharma_database"
    MILVUS_TIMEOUT = 10
    
    # Text Splitting Configuration - Adjusted for embedding model context length
    CHUNK_SIZE = 200
    CHUNK_OVERLAP = 20
    
    # Retrieval Configuration
    SEARCH_K = 5
    MAX_TOKENS = 300  # Adjusted for small model context length
    TEMPERATURE = 0.7
    
    # No-Think Mode Configuration
    NO_THINK_MODE = False
    
    # Create temporary directory
    os.makedirs("./temp", exist_ok=True)

# Initialize Milvus client
client = MilvusClient(
    uri=Config.MILVUS_URI,
    token=Config.MILVUS_TOKEN,
    timeout=Config.MILVUS_TIMEOUT
)

# Ensure the database exists
databases = client.list_databases()
if Config.MILVUS_DATABASE not in databases:
    client.create_database(Config.MILVUS_DATABASE)

# Switch to the database
client.using_database(Config.MILVUS_DATABASE)

# Initialize local embedding model
# Pointing to local vLLM service, model name matches served-model-name
embedding_model = OpenAIEmbeddings(
    model=Config.EMBEDDING_MODEL_NAME,
    api_key=Config.EMBEDDING_API_KEY,
    base_url=Config.EMBEDDING_API_BASE
)

# Initialize Milvus vector store using langchain_milvus
db = Milvus(
    embedding_function=embedding_model,
    collection_name=Config.MILVUS_COLLECTION_NAME,
    connection_args={
        "uri": Config.MILVUS_URI,
        "token": Config.MILVUS_TOKEN,
        "db_name": Config.MILVUS_DATABASE,
        "timeout": Config.MILVUS_TIMEOUT
    }
)