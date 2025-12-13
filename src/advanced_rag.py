"""
Advanced RAG System for Healing Vault
Combines vector search, keyword search, and AI reranking for better retrieval
"""

import chromadb
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import numpy as np

# Configuration
DB_PATH = "./data/chroma_db"
EMBEDDING_MODEL = "llama3.1:8b"
LLM_MODEL = "llama3.1:8b"

class AdvancedRAG:
    """Enhanced retrieval system with hybrid search and reranking"""
    
    def __init__(self):
        """Initialize the RAG system"""
        print("📚 Loading advanced RAG system...")
        
        # Load vector database
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        self.chroma_client = chromadb.PersistentClient(path=DB_PATH)
        self.vectorstore = Chroma(
            client=self.chroma_client,
            collection_name="healing_vault_books",
            embedding_function=self.embeddings
        )
        
        # Load all documents for BM25 keyword search
        self.collection = self.chroma_client.get_collection("healing_vault_books")
        all_data = self.collection.get()
        
        self.documents = all_data['documents']
        self.metadatas = all_data['metadatas']
        self.ids = all_data['ids']
        
        # Create BM25 index for keyword search
        print("🔍 Building keyword search index...")
        tokenized_docs = [doc.lower().split() for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_docs)
        
        print("✓ RAG system ready\n")
    
    def hybrid_search(self, query, k=10):
        """
        Combine vector similarity and keyword matching
        """
        # Vector search (semantic similarity)
        vector_results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        # Keyword search (BM25)
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        
        # Get top k BM25 results
        top_bm25_indices = np.argsort(bm25_scores)[-k:][::-1]
        
        # Combine results with hybrid scoring
        results = {}
        
        # Add vector results (normalize scores to 0-1 range)
        max_vector_score = max([score for _, score in vector_results]) if vector_results else 1
        for doc, score in vector_results:
            doc_text = doc.page_content
            normalized_score = 1 - (score / max_vector_score)
            
            if doc_text not in results:
                results[doc_text] = {
                    'document': doc,
                    'metadata': doc.metadata,
                    'vector_score': normalized_score,
                    'bm25_score': 0
                }
        
        # Add BM25 results (normalize scores)
        max_bm25_score = max(bm25_scores) if max(bm25_scores) > 0 else 1
        for idx in top_bm25_indices:
            doc_text = self.documents[idx]
            normalized_score = bm25_scores[idx] / max_bm25_score
            
            if doc_text in results:
                results[doc_text]['bm25_score'] = normalized_score
            else:
                doc = Document(page_content=doc_text, metadata=self.metadatas[idx])
                results[doc_text] = {
                    'document': doc,
                    'metadata': self.metadatas[idx],
                    'vector_score': 0,
                    'bm25_score': normalized_score
                }
        
        # Calculate hybrid scores (weighted combination)
        for doc_text in results:
            vector_weight = 0.7
            keyword_weight = 0.3
            
            results[doc_text]['hybrid_score'] = (
                vector_weight * results[doc_text]['vector_score'] +
                keyword_weight * results[doc_text]['bm25_score']
            )
        
        # Sort by hybrid score
        sorted_results = sorted(
            results.values(),
            key=lambda x: x['hybrid_score'],
            reverse=True
        )
        
        return [(r['document'], r['metadata'], r['hybrid_score']) for r in sorted_results[:k]]
    
    def rerank_with_llm(self, query, candidates, top_k=3):
        """Use LLM to rerank candidates based on relevance"""
        print(f"🧠 Reranking {len(candidates)} candidates with AI...")
        
        llm = Ollama(model=LLM_MODEL, temperature=0.3)
        
        # Build reranking prompt
        passages_text = ""
        for i, (doc, meta, score) in enumerate(candidates):
            book_title = meta.get('book_title', 'Unknown')
            page = meta.get('page', '?')
            preview = doc.page_content[:300]
            passages_text += f"\n[{i}] From '{book_title}' (page {page}):\n{preview}...\n"
        
        prompt = f"""You are a clinical psychology expert. Rate how relevant each passage is to this user's concern.

User's concern: "{query}"

Passages:
{passages_text}

Respond with ONLY a comma-separated list of passage numbers in order of relevance (most relevant first).
Example: 2,5,1,7,3

Your ranking (numbers only):"""
        
        response = llm.invoke(prompt).strip()
        
        # Parse rankings
        try:
            rankings = [int(x.strip()) for x in response.split(',') if x.strip().isdigit()]
            reranked = [candidates[i] for i in rankings if i < len(candidates)]
            
            # Add any missing candidates at the end
            included_indices = set(rankings)
            for i, candidate in enumerate(candidates):
                if i not in included_indices:
                    reranked.append(candidate)
            
            return reranked[:top_k]
        except:
            print("⚠ Reranking parse failed, using hybrid scores")
            return candidates[:top_k]
    
    def smart_search(self, query, top_k=3, use_reranking=True):
        """Full pipeline: hybrid search + optional AI reranking"""
        # Step 1: Hybrid search
        candidates = self.hybrid_search(query, k=10)
        print(f"✓ Hybrid search found {len(candidates)} candidates")
        
        # Step 2: Optional reranking
        if use_reranking:
            final_results = self.rerank_with_llm(query, candidates, top_k=top_k)
        else:
            final_results = candidates[:top_k]
        
        print(f"✓ Returning top {len(final_results)} results\n")
        return [(doc, meta) for doc, meta, score in final_results]


def test_advanced_rag():
    """Test the advanced RAG system"""
    print("=" * 70)
    print("ADVANCED RAG SYSTEM TEST")
    print("=" * 70)
    
    rag = AdvancedRAG()
    
    # Test queries
    test_queries = [
        "panic attack and nervous system freeze response",
        "attachment anxiety in relationships",
        "childhood trauma affecting adult relationships"
    ]
    
    for query in test_queries:
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)
        
        results = rag.smart_search(query, top_k=3, use_reranking=True)
        
        print("TOP 3 RESULTS:")
        for i, (doc, meta) in enumerate(results, 1):
            print(f"\n{i}. {meta['book_title']} (page {meta.get('page', '?')})")
            print(f"   {doc.page_content[:200]}...")
        
        print("\n" + "-" * 70)


if __name__ == "__main__":
    test_advanced_rag()