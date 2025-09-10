from config import Config
import requests
import json

class DocumentReranker:
    """Document reranker for relevance-based reordering of retrieved documents.
    
    Uses Qwen3-Reranker-0.6B model deployed via vllm to rerank documents 
    based on semantic relevance to the query and document content, helping 
    improve the quality of retrieval results in RAG systems.
    """
    def __init__(self):
        """Initialize the reranker."""
        self.rerank_api_url = f"{Config.RERANK_API_BASE}/rerank"
        
    def rerank_docs(self, query, docs):
        """Rerank documents based on the query.
        
        Args:
            query (str): User query
            docs (list): List of retrieved documents
        
        Returns:
            list: Reranked list of documents
        """
        if not Config.RERANK_ENABLED or not docs or len(docs) <= 1:
            # If reranking is not enabled or there are not enough documents, return the original list directly
            return docs
        
        try:
            # Prepare request data
            request_data = {
                "model": Config.RERANK_MODEL_NAME,
                "query": query,
                "documents": [doc.page_content for doc in docs],
                "top_n": Config.RERANK_TOP_K
            }
            
            # Send request to vllm rerank service
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {Config.RERANK_API_KEY}"
            }
            
            response = requests.post(
                self.rerank_api_url,
                headers=headers,
                data=json.dumps(request_data)
            )
            
            # Check response status
            if response.status_code != 200:
                print(f"Rerank API request failed with status code {response.status_code}: {response.text}")
                return docs
            
            # Parse response
            rerank_results = response.json()
            
            # Get reranked document indices
            if "results" in rerank_results and rerank_results["results"]:
                # Create reranked document list
                reranked_docs = []
                for result in rerank_results["results"]:
                    # Ensure index is valid
                    if "index" in result and 0 <= result["index"] < len(docs):
                        reranked_docs.append(docs[result["index"]])
                
                # If reranked documents were successfully obtained, return them
                if reranked_docs:
                    return reranked_docs
                else:
                    print("No valid reranked documents found in response")
            else:
                print("Invalid rerank API response format")
                print(f"Response: {rerank_results}")
                
            # If there's an error in reranking process, return original document list
            return docs
        except Exception as e:
            print(f"Error during reranking: {e}")
            # If there's an error in reranking process, return original document list
            return docs

# Create global reranker instance
reranker = DocumentReranker()

def rerank_documents(query, docs):
    """Convenience function for reranking retrieved documents.
    
    Args:
        query (str): User query
        docs (list): List of retrieved documents
    
    Returns:
        list: Reranked list of documents
    """
    return reranker.rerank_docs(query, docs)