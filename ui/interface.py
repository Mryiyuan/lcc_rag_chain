import streamlit as st
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_chain.chain import run_rag_chain_stream
from vector_db.add_documents import add_to_db
from vector_db.chroma_db import delete_documents_by_file_id
from config import Config

# 初始化聊天历史
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 初始化已上传文件列表
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []


def render_main_page():
    """Render the main page of the application with chat interface."""
    st.set_page_config(page_title="Retrieval System", page_icon=":microscope:")
    st.title("Retrieval System")
    st.subheader("Chat with your knowledge base")

    # 显示聊天历史
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    # 聊天输入框
    if prompt := st.chat_input("Ask a question"):
        # 添加用户消息到历史
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 显示助手响应
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # 创建流式输出的占位符
                message_placeholder = st.empty()
                full_response = ""
                
                # 流式获取响应，传入聊天历史
                for chunk in run_rag_chain_stream(query=prompt, chat_history=st.session_state.chat_history):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                
                # 显示最终响应
                message_placeholder.markdown(full_response)
                
                # 添加助手响应到历史
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})


def render_sidebar():
    """Render the sidebar of the Retrieval System application."""
    with st.sidebar:
        st.title("Model Configuration")
        st.info("Using local vLLM with Qwen3-0.6B model")
        # st.write(f"Base URL: {Config.VLLM_API_BASE}")
        st.write(f"Model: {Config.VLLM_MODEL_NAME}")
        
        # 添加无思考模式开关
        no_thought_mode = st.toggle("Enable No-Thought Mode", value=Config.NO_THINK_MODE)
        if no_thought_mode != Config.NO_THINK_MODE:
            Config.NO_THINK_MODE = no_thought_mode
            st.success(f"No-Thought Mode {'enabled' if no_thought_mode else 'disabled'}")
        
        # 聊天历史管理
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
        
        # 已上传文件管理
        st.markdown("---")
        st.subheader("Uploaded Files")
        
        # 格式化文件大小的辅助函数
        def format_size(size_bytes):
            """将字节大小格式化为人类可读的格式"""
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1048576:
                return f"{size_bytes/1024:.2f} KB"
            else:
                return f"{size_bytes/1048576:.2f} MB"
        
        # 显示已上传文件并提供删除选项
        if st.session_state.uploaded_files:
            for file in st.session_state.uploaded_files:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{file['name']}**")
                    st.caption(f"大小: {format_size(file['size'])}")
                    st.caption(f"上传时间: {file['upload_time']}")
                with col2:
                    if st.button("删除", key=f"delete_{file['id']}"):
                        # 从向量数据库中删除文档
                        success = delete_documents_by_file_id(file['id'])
                        if success:
                            # 从session state中移除文件
                            st.session_state.uploaded_files = [
                                f for f in st.session_state.uploaded_files if f['id'] != file['id']
                            ]
                            st.success(f"成功删除 '{file['name']}' 及其向量")
                            # 刷新页面更新列表
                            st.rerun()
                        else:
                            st.error(f"删除 '{file['name']}' 的向量失败")
        else:
            st.info("尚未上传文件。")
        
        # 侧边栏页脚
        st.write("Built with ❤️ by [LiChenchen]()")