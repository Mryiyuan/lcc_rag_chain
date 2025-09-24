import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入配置和数据库模块
from config import Config, db, embedding_model


def test_milvus_connection():
    """简单测试Milvus连接和功能"""
    try:
        print("开始测试Milvus连接和功能...")
        
        # 测试嵌入模型
        print("测试嵌入模型...")
        test_embedding = embedding_model.embed_query("这是一个测试查询")
        print(f"嵌入模型正常工作，嵌入维度: {len(test_embedding)}")
        
        # 测试数据库连接 - 添加一个简单文档
        print("测试添加文档...")
        from langchain.docstore.document import Document
        test_docs = [Document(
            page_content="这是一个测试文档", 
            metadata={"file_name": "test_doc.txt", "source": "test"}
        )]
        
        doc_ids = db.add_documents(test_docs)
        print(f"成功添加文档，文档ID: {doc_ids}")
        
        # 测试检索功能
        print("测试检索功能...")
        retriever = db.as_retriever(search_kwargs={"k": 1})
        results = retriever.invoke("测试")
        print(f"检索结果数量: {len(results)}")
        if results:
            print(f"检索结果内容: {results[0].page_content}")
            print(f"检索结果元数据: {results[0].metadata}")
        
        # 清理测试数据
        if doc_ids:
            print("清理测试数据...")
            for doc_id in doc_ids:
                db.delete([doc_id])
            print("测试数据已清理")
        
        print("所有Milvus测试通过！")
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_milvus_connection()
    sys.exit(0 if success else 1)