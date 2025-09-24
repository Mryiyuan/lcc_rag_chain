# RAG Chain - 通用检索增强生成应用程序

[English](README.md) | [中文](README_CN.md)

lcc RAG Chain 是一个专为通用文档问答设计的检索增强生成（RAG）应用程序。它允许用户就任何主题提出问题，并根据上传的文档获得准确、符合上下文的答案。

## 功能特点

- **文档上传**：上传 PDF 文档以增强知识库
- **基于 RAG 的问答**：就任何主题提问并获得基于上下文的答案
- **模块化设计**：结构清晰、职责分明的代码库
- **参数可配置**：通过配置轻松自定义应用程序行为
- **Streamlit 界面**：用户友好的 Web 交互界面
- **Milvus 向量数据库**：高性能、可扩展的向量搜索引擎，提供高效文档检索
- **Docker 部署**：一键容器化，省心省显存  
  - 全部模型（LLM / embedding / reranker）基于 [vllm/vllm-openai](https://hub.docker.com/r/vllm/vllm-openai) 官方镜像构建，自动 tensor-parallel，显存占用最低。  
  - 本地测试：`docker compose up -d` 即可拉起完整服务；生产环境只需改 `.env` 中的模型名或 `OPENAI_BASE_URL`，立即切换任意兼容 OpenAI 接口的模型（GPT、Claude、Qwen、Baichuan 等）。  
  - 提供 `Dockerfile` & `docker-compose.yml`，支持 CPU 调试 / GPU 推理双模式，后续上云零改动。

## 项目结构

```
lcc_rag_chain/
├── .gitignore             # Git 忽略文件
├── LICENSE                # 许可证文件
├── README.md              # 英文文档
├── README_CN.md           # 中文文档
├── main.py                # 应用程序入口点，支持参数配置
├── config.py              # 配置参数
├── requirements.txt       # Python 依赖项
├── data_loader/           # 文档加载模块
│   ├── __init__.py
│   └── pdf_loader.py      # PDF 文档加载功能
├── text_splitter/         # 文本分割模块
│   ├── __init__.py
│   └── splitter.py        # 文本分割功能
├── embedding/             # 嵌入模型模块
│   ├── __init__.py
│   └── embedder.py        # 嵌入模型实现
├── vector_db/             # 向量数据库操作模块
│   ├── __init__.py
│   ├── milvus_db.py       # Milvus 数据库操作
│   └── add_documents.py   # 文档添加功能
├── rag_chain/             # RAG 链操作模块
│   ├── __init__.py
│   └── chain.py           # RAG 链实现
├── ui/                    # 用户界面模块
│   ├── __init__.py
│   └── interface.py       # Streamlit 界面实现
├── utils/                 # 工具函数
│   ├── __init__.py
│   ├── helpers.py         # 辅助函数
│   └── reranker.py        # 文档重排序器实现
├── temp/                  # 临时文件目录
├── test_milvus.py         # Milvus 综合测试脚本
├── test_milvus_connection.py # Milvus 连接测试
├── test_milvus_simple.py  # Milvus 简化测试脚本
└── docker-compose/        # Docker Compose 配置
    ├── Qwen3-0.6B-GPTQ-Int8/  # Qwen3 LLM 模型 Docker 配置
    ├── Qwen3-Embedding-0.6B/  # Qwen3 Embedding 模型 Docker 配置
    └── Qwen3-Reranker-0.6B/   # Qwen3 Reranker 模型 Docker 配置
```

## 安装说明

1. 克隆代码库：
   ```bash
   git clone https://github.com/Mryiyuan/lcc_rag_chain.git
   cd lcc_rag_chain
   ```

2. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 配置说明

应用程序可以通过 `config.py` 文件或命令行参数进行配置：

### 配置参数

- `EMBEDDING_API_BASE`：嵌入模型 API 基础 URL
- `EMBEDDING_API_KEY`：嵌入服务的 API 密钥
- `EMBEDDING_MODEL_NAME`：嵌入模型名称
- `VLLM_API_BASE`：vLLM API 基础 URL
- `CHUNK_SIZE`：文档分割的文本块大小
- `CHUNK_OVERLAP`：文档分割的文本块重叠大小
- `SEARCH_K`：相似性搜索中检索的文档数量
- `MAX_TOKENS`：LLM 响应的最大 token 数
- `TEMPERATURE`：LLM 响应生成的温度参数
- `MILVUS_URI`：Milvus 服务器连接 URI
- `MILVUS_TOKEN`：Milvus 认证令牌
- `MILVUS_DATABASE`：Milvus 数据库名称
- `MILVUS_COLLECTION_NAME`：Milvus 集合名称
- `MILVUS_TIMEOUT`：Milvus 连接超时时间（秒）

### 命令行参数

- `--host`：运行应用程序的主机地址（默认：localhost）
- `--port`：运行应用程序的端口号（默认：8501）
- `--embedding-api-base`：嵌入模型 API 基础 URL
- `--vllm-api-base`：vLLM API 基础 URL
- `--chunk-size`：文档分割的文本块大小
- `--chunk-overlap`：文档分割的文本块重叠大小
- `--search-k`：相似性搜索中检索的文档数量

## 使用方法

1. 启动应用程序：
   ```bash
   streamlit run main.py
   ```

2. 或者使用自定义参数启动：
   ```bash
   streamlit run main.py --server.port 8502
   ```

3. 打开浏览器并访问 `http://localhost:8501`（或您的自定义端口）

4. 使用界面可以：
   - 在主文本区域提问
   - 在侧边栏上传 PDF 文档
   - 查看模型配置信息

### 数据加载器 (`data_loader/`)
处理 PDF 文档的加载：
- `save_temp_file()`：将上传的文件保存到临时位置
- `remove_temp_file()`：处理完成后删除临时文件
- `load_pdf_document()`：使用 PyPDFLoader 加载 PDF 文档

### 文本分割器 (`text_splitter/`)
处理文档的文本分割：
- `create_recursive_splitter()`：创建递归字符文本分割器
- `split_documents()`：将文档分割成较小的块

### 向量数据库 (`vector_db/`)
处理 Milvus 向量数据库操作：
- `add_documents_to_db()`：向 Milvus 数据库添加文档
- `get_retriever()`：获取用于相似性搜索的检索器对象
- `add_to_db()`：处理并添加上传的文件到数据库
- `delete_documents_by_file_id()`：根据文件标识符从数据库删除文档

### RAG 链 (`rag_chain/`)
实现检索增强生成链：
- `run_rag_chain()`：使用 RAG 链处理查询，包括文档检索和 LLM 生成
- `get_prompt_template()`：为 LLM 交互创建提示模板

### 用户界面 (`ui/`)
实现 Streamlit 用户界面：
- `render_main_page()`：渲染主应用页面
- `render_sidebar()`：渲染包含配置和文件上传的侧边栏
- `clear_messages()`：清除聊天历史

### 嵌入模型 (`embedding/`)
处理文本嵌入功能：
- `get_embedding_model()`：返回配置的嵌入模型实例

### 工具函数 (`utils/`)
包含辅助函数：
- `format_docs()`：将文档对象格式化为单个字符串
- `get_reranker()`：返回用于改进搜索结果的重排序器模型

### 测试脚本
项目包含多个测试脚本，用于验证 Milvus 数据库功能：
- `test_milvus_simple.py`：Milvus 连接和基本操作的简化测试
- `test_milvus_connection.py`：Milvus 连接和配置测试
- `test_milvus.py`：Milvus 数据库操作的综合测试

### 运行测试
要验证 Milvus 是否配置正确且功能正常，您可以运行测试脚本：

```bash
# 运行简化版 Milvus 测试
python test_milvus_simple.py

# 运行 Milvus 连接测试
python test_milvus_connection.py

# 运行综合版 Milvus 测试
python test_milvus.py
```

这些测试将验证：
- Milvus 服务器连接
- 嵌入模型功能
- 向 Milvus 添加文档
- 文档检索和搜索
- 文档删除

## 依赖要求

- Python 3.8+
- Streamlit
- Langchain
- Langchain Milvus
- PyMilvus
- OpenAI Python SDK
- PyPDF
- sentence-transformers
- loguru

详细依赖项请参见 `requirements.txt` 文件。

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 许可证

本项目采用 MIT 许可证 - 详情请见 LICENSE 文件。


## Docker 部署

`docker-compose` 目录包含了将 Qwen3 模型作为 Docker 容器运行的配置。这提供了一种便捷的方式来部署所需的模型服务。

### 前提条件
- 系统已安装 Docker 和 Docker Compose
- 具有 CUDA 支持的 NVIDIA GPU（用于 GPU 加速）
- 已安装 NVIDIA Container Toolkit

### 可用配置

1. **Qwen3-0.6B-GPTQ-Int8**：用于运行 Qwen3 语言模型（带有 GPTQ 量化）的配置
2. **Qwen3-Embedding-0.6B**：用于运行 Qwen3 嵌入模型的配置
3. **Qwen3-Reranker-0.6B**：用于运行 Qwen3 重排序模型的配置

### 使用方法

1. 首先，确保您在本地有 Qwen3 模型。默认配置假设模型位于以下位置：
   - Qwen3-0.6B-GPTQ-Int8：`D:\model\Qwen3-0.6B-GPTQ-Int8`
   - Qwen3-Embedding-0.6B：`D:/model/Qwen/Qwen3-Embedding-0.6B`
   - Qwen3-Reranker-0.6B：`D:/model/Qwen/Qwen3-Reranker-0.6B`

   **注意**：如果您的模型位于不同的目录，需要更新相应 `docker-compose.yml` 文件中的卷映射。

2. 启动所需的服务：

   对于语言模型：
   ```bash
   cd docker-compose/Qwen3-0.6B-GPTQ-Int8
   docker-compose up -d
   ```

   对于嵌入模型：
   ```bash
   cd docker-compose/Qwen3-Embedding-0.6B
   docker-compose up -d
   ```

   对于重排序模型：
   ```bash
   cd docker-compose/Qwen3-Reranker-0.6B
   docker-compose up -d
   ```

3. 验证服务是否正常运行：
   ```bash
   docker-compose ps
   ```

4. 更新应用程序配置（`config.py` 或通过命令行参数）以指向这些服务：
   - LLM 服务：`http://localhost:8800/v1`
   - Embedding 服务：`http://localhost:50001/v1`
   - Reranker 服务：`http://localhost:60001/v1`

### 配置说明
- 所有配置均使用 `vllm/vllm-openai:v0.10.1.1` 镜像
- API 密钥设置为默认值（`sk-123456`、`sk123456`）用于测试目的
- GPU 内存利用率和其他参数针对典型使用场景进行了优化
- 嵌入服务使用 `pooling` 运行器来生成嵌入向量