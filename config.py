import os
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Configuration parameters
class Config:
    # API配置
    EMBEDDING_API_BASE = "http://host.docker.internal:50001/v1"
    EMBEDDING_API_KEY = "sk123456"
    EMBEDDING_MODEL_NAME = "qwen3-ebd-0d6"
    
    # vLLM配置
    VLLM_API_BASE = "http://host.docker.internal:8800/v1"
    VLLM_API_KEY = "sk-123456"
    VLLM_MODEL_NAME = "Qwen3-0.6B-GPTQ-Int8"
    
    # 数据库配置
    CHROMA_DB_PATH = "./chroma_db"
    PHARMA_DB_PATH = "./pharma_db"
    COLLECTION_NAME = "pharma_database"
    
    # 文本分割配置 - 已调整为适合嵌入模型的上下文长度
    CHUNK_SIZE = 200
    CHUNK_OVERLAP = 20
    
    # 检索配置
    SEARCH_K = 5
    MAX_TOKENS = 300  # 已调整为适合小模型的上下文长度
    TEMPERATURE = 0.7
    
    # 无思考模式配置
    NO_THINK_MODE = False
    
    # 创建临时目录
    os.makedirs("./temp", exist_ok=True)

# Initialize local embedding model
# 指向本机 vLLM 服务，模型名和 served-model-name 保持一致
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