# PharmaQuery - 医药行业洞察检索系统

PharmaQuery 是一个专为医药行业设计的检索增强生成（RAG）应用程序。它允许用户就医药相关主题提出问题，并根据上传的研究文档获得准确、符合上下文的答案。

## 功能特点

- **文档上传**：上传 PDF 研究文档以增强知识库
- **基于 RAG 的问答**：就医药主题提问并获得基于上下文的答案
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
├── pharma_db/             # 持久化 Chroma 数据库
└── chroma_db/             # Chroma 数据库文件
```

## 安装说明

1. 克隆代码库：
   ```bash
   git clone <repository-url>
   cd rag_chain
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
   - 在侧边栏上传 PDF 研究文档
   - 查看模型配置信息

## 模块说明

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