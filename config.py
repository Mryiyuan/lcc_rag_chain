import os
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

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
    CHROMA_DB_PATH = "./chroma_db"
    PHARMA_DB_PATH = "./pharma_db"
    COLLECTION_NAME = "pharma_database"
    
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

# Initialize local embedding model
# Pointing to local vLLM service, model name matches served-model-name
embedding_model = OpenAIEmbeddings(
    openai_api_base=Config.EMBEDDING_API_BASE,
    openai_api_key=Config.EMBEDDING_API_KEY,
    model=Config.EMBEDDING_MODEL_NAME
)

# Initialize Chroma client
client = chromadb.PersistentClient(
    path=Config.CHROMA_DB_PATH,
    settings=chromadb.Settings(allow_reset=True),
    tenant=chromadb.DEFAULT_TENANT,
    database=chromadb.DEFAULT_DATABASE,
)

# Initialize pharma database
db = Chroma(collection_name=Config.COLLECTION_NAME,
            embedding_function=embedding_model,
            persist_directory=Config.PHARMA_DB_PATH)