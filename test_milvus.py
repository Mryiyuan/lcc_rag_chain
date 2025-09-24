import sys
import os
from loguru import logger

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入配置和数据库模块
from config import Config, db, embedding_model

logger.remove()
logger.add(sys.stdout, level="DEBUG")


def test_milvus_connection():
    """测试Milvus连接和基本功能"""
    try:
        logger.info("开始测试Milvus连接和功能...")
        
        # 测试嵌入模型
        logger.info("测试嵌入模型...")
        test_embedding = embedding_model.embed_query("这是一个测试查询")
        logger.info(f"嵌入模型正常工作，嵌入维度: {len(test_embedding)}")
        
        # 测试数据库连接 - 添加一个简单文档
        logger.info("测试添加文档...")
        from langchain.docstore.document import Document
        test_docs = [Document(
            page_content="这是一个测试文档", 
            metadata={"file_name": "test_doc.txt", "source": "test"}
        )]
        
        doc_ids = db.add_documents(test_docs)
        logger.info(f"成功添加文档，文档ID: {doc_ids}")
        
        # 测试检索功能
        logger.info("测试检索功能...")
        retriever = db.as_retriever(search_kwargs={"k": 1})
        results = retriever.invoke("测试")
        logger.info(f"检索结果数量: {len(results)}")
        if results:
            logger.info(f"检索结果内容: {results[0].page_content}")
            logger.info(f"检索结果元数据: {results[0].metadata}")
        
        # 清理测试数据
        if doc_ids:
            logger.info("清理测试数据...")
            for doc_id in doc_ids:
                db.delete([doc_id])
            logger.info("测试数据已清理")
        
        logger.success("所有Milvus测试通过！")
        return True
        
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = test_milvus_connection()
    sys.exit(0 if success else 1)