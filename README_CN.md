# RAG Chain - 通用检索增强生成应用程序

RAG Chain 是一个专为通用文档问答设计的检索增强生成（RAG）应用程序。它允许用户就任何主题提出问题，并根据上传的文档获得准确、符合上下文的答案。

## 功能特点

- **文档上传**：上传 PDF 文档以增强知识库
- **基于 RAG 的问答**：就任何主题提问并获得基于上下文的答案
- **模块化设计**：结构清晰、职责分明的代码库
- **参数可配置**：通过配置轻松自定义应用程序行为
- **Streamlit 界面**：用户友好的 Web 交互界面

## 项目结构

```
rag_chain/
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
├── vector_db/             # 向量数据库操作模块
│   ├── __init__.py
│   ├── chroma_db.py       # Chroma 数据库操作
│   └── add_documents.py   # 文档添加功能
├── rag_chain/             # RAG 链操作模块
│   ├── __init__.py
│   └── chain.py           # RAG 链实现
├── ui/                    # 用户界面模块
│   ├── __init__.py
│   └── interface.py       # Streamlit 界面实现
├── utils/                 # 工具函数
│   ├── __init__.py
│   └── helpers.py         # 辅助函数
├── temp/                  # 临时文件目录
├── chroma_db/             # Chroma 数据库文件
└── docker-compose/        # Docker Compose 配置
    ├── Qwen3-0.6B-GPTQ-Int8/  # Qwen3 LLM 模型 Docker 配置
    └── Qwen3-Embedding-0.6B/  # Qwen3 Embedding 模型 Docker 配置
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
- `VLLM_API_BASE`：vLLM API 基础 URL
- `CHUNK_SIZE`：文档分割的文本块大小
- `CHUNK_OVERLAP`：文档分割的文本块重叠大小
- `SEARCH_K`：相似性搜索中检索的文档数量
- `MAX_TOKENS`：LLM 响应的最大 token 数
- `TEMPERATURE`：LLM 响应生成的温度参数

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
   streamlit run main.py --port 8502 --chunk-size 1024
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
处理向量数据库操作：
- `add_documents_to_db()`：向 Chroma 数据库添加文档
- `get_retriever()`：获取用于相似性搜索的检索器对象
- `add_to_db()`：处理并添加上传的文件到数据库

### RAG 链 (`rag_chain/`)
实现检索增强生成链：
- `run_rag_chain()`：使用 RAG 链处理查询

### 用户界面 (`ui/`)
实现 Streamlit 用户界面：
- `render_main_page()`：渲染主应用页面
- `render_sidebar()`：渲染包含配置和文件上传的侧边栏

### 工具函数 (`utils/`)
包含辅助函数：
- `format_docs()`：将文档对象格式化为单个字符串

## 依赖要求

- Python 3.8+
- Streamlit
- Langchain
- ChromaDB
- OpenAI Python SDK
- PyPDF2

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

### 使用方法

1. 首先，确保您在本地有 Qwen3 模型。默认配置假设模型位于以下位置：
   - Qwen3-0.6B-GPTQ-Int8：`D:\model\Qwen3-0.6B-GPTQ-Int8`
   - Qwen3-Embedding-0.6B：`D:/model/Qwen/Qwen3-Embedding-0.6B`

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

3. 验证服务是否正常运行：
   ```bash
   docker-compose ps
   ```

4. 更新应用程序配置（`config.py` 或通过命令行参数）以指向这些服务：
   - LLM 服务：`http://localhost:8800/v1`
   - Embedding 服务：`http://localhost:50001/v1`

### 配置说明
- 两种配置均使用 `vllm/vllm-openai:v0.10.1.1` 镜像
- API 密钥设置为默认值（`sk-123456` 和 `sk123456`）用于测试目的
- GPU 内存利用率和其他参数针对典型使用场景进行了优化
- 嵌入服务使用 `pooling` 运行器来生成嵌入向量