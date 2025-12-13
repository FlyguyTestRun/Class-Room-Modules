"""
The Trauma Guide - First Friend Prototype
Demonstrates RAG-powered therapeutic response using embedded psychology books
"""

import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
import chromadb

# Configuration
DB_PATH = "./data/chroma_db"
EMBEDDING_MODEL = "llama3.1:8b"
LLM_MODEL = "llama3.1:8b"

def load_vectorstore():
    """Load the existing ChromaDB vector database"""
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    
    vectorstore = Chroma(
        client=chroma_client,
        collection_name="healing_vault_books",
        embedding_function=embeddings
    )
    
    return vectorstore

def trauma_guide_response(user_entry, vectorstore):
    """Generate Trauma Guide response with book citations"""
    
    # Step 1: Search books for relevant passages
    print("\n🔍 Searching your psychology library...")
    relevant_docs = vectorstore.similarity_search(user_entry, k=3)
    
    # Step 2: Build context from retrieved passages
    context = "\n\n".join([
        f"From '{doc.metadata['book_title']}' (page {doc.metadata.get('page', '?')}):\n{doc.page_content[:500]}..."
        for doc in relevant_docs
    ])
    
    print(f"✓ Found {len(relevant_docs)} relevant passages\n")
    
    # Step 3: Build the prompt for Trauma Guide
    system_prompt = """You are The Trauma Guide - a compassionate somatic therapist who embodies yoga wisdom. 

Your voice draws from:
- Bessel van der Kolk's "The Body Keeps the Score" (trauma lives in the body)
- Peter Levine's somatic experiencing (nervous system regulation)
- Gabor Maté's compassionate inquiry (trauma as disconnection from self)

Core principles:
- "Your body is speaking what your mouth cannot say"
- Trauma responses (freeze, fight, flight) are protective, not weakness
- The nervous system can be retrained through gentle, titrated steps
- Acknowledge both the wound and the survival strategy

Respond in 4-6 sentences. Be warm but direct. Name what you see in their nervous system. Reference the book passages provided to ground your response in clinical wisdom, citing the book title naturally (e.g., "Van der Kolk describes this as...").

DO NOT diagnose. DO offer psychoeducation and nervous system language."""

    user_prompt = f"""Journal Entry:
"{user_entry}"

Relevant passages from psychology books:
{context}

Respond as The Trauma Guide with compassion and somatic awareness. Reference the books naturally when relevant."""

    # Step 4: Generate response using Ollama
    print("🧠 The Trauma Guide is responding...\n")
    llm = Ollama(model=LLM_MODEL, temperature=0.7)
    
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    response = llm.invoke(full_prompt)
    
    return response, relevant_docs

def main():
    """Test the Trauma Guide with a sample entry"""
    print("=" * 70)
    print("HEALING VAULT - Trauma Guide Prototype")
    print("=" * 70)
    
    # Load the vector database
    print("\n📚 Loading your psychology library...")
    vectorstore = load_vectorstore()
    print("✓ Library loaded\n")
    
    # Sample journal entry (you can change this)
    test_entry = """I had a panic attack today when my boss raised his voice in the meeting. 
I couldn't breathe, my chest got tight, and I felt like I was going to pass out. 
I hate that I react this way - everyone else seemed fine but I just froze. 
I feel so weak and broken."""
    
    print("=" * 70)
    print("JOURNAL ENTRY:")
    print("=" * 70)
    print(test_entry)
    print("\n" + "=" * 70)
    
    # Get Trauma Guide response
    response, sources = trauma_guide_response(test_entry, vectorstore)
    
    print("=" * 70)
    print("THE TRAUMA GUIDE RESPONDS:")
    print("=" * 70)
    print(response)
    
    print("\n" + "=" * 70)
    print("SOURCES REFERENCED:")
    print("=" * 70)
    for i, doc in enumerate(sources, 1):
        print(f"\n{i}. {doc.metadata['book_title']} (page {doc.metadata.get('page', '?')})")
        print(f"   Preview: {doc.page_content[:200]}...")

if __name__ == "__main__":
    main()