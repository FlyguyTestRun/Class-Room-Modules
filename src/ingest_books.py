"""
PDF Ingestion Pipeline for Healing Vault
Processes psychology books into ChromaDB vector database for RAG retrieval
"""

import os
from pathlib import Path
import chromadb
from chromadb.config import Settings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration
BOOKS_PATH = r"C:\Users\GameRoom PC Shaw1\OneDrive\Desktop\Psycology Books\Core Books"
DB_PATH = "./data/chroma_db"  # Where vector database will be stored
EMBEDDING_MODEL = "llama3.1:8b"  # Model for creating embeddings

def load_pdfs(books_dir):
    """Load all PDFs from directory and extract text with metadata"""
    print(f"📚 Loading PDFs from {books_dir}...")
    
    documents = []
    pdf_files = list(Path(books_dir).glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files")
    
    for pdf_path in pdf_files:
        try:
            print(f"  Loading: {pdf_path.name}")
            loader = PyPDFLoader(str(pdf_path))
            pages = loader.load()
            
            # Add book title metadata to each page
            for page in pages:
                page.metadata["source_file"] = pdf_path.name
                page.metadata["book_title"] = pdf_path.stem  # Filename without .pdf
            
            documents.extend(pages)
            print(f"    ✓ Loaded {len(pages)} pages")
            
        except Exception as e:
            print(f"    ✗ Error loading {pdf_path.name}: {str(e)}")
            continue
    
    print(f"\n✓ Total pages loaded: {len(documents)}")
    return documents

def chunk_documents(documents):
    """Split documents into smaller chunks for better retrieval"""
    print("\n📄 Splitting documents into chunks...")
    
    # This splitter tries to keep paragraphs together when possible
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,  # Each chunk ~3000 characters (6-9 paragraphs)
        chunk_overlap=300,  # 300 char overlap to maintain context
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"✓ Created {len(chunks)} chunks")
    return chunks

def create_vectorstore(chunks):
    """Create embeddings and store in ChromaDB with real progress tracking"""
    print("\n🧠 Creating embeddings with Ollama...")
    print(f"⏳ Processing {len(chunks)} chunks...")
    print("This uses your CPU—expect 15-30 minutes on a fast desktop\n")
    
    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    # Create vector database directory
    os.makedirs(DB_PATH, exist_ok=True)
    
    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    
    # Create or get collection
    try:
        collection = chroma_client.get_collection(name="healing_vault_books")
        print("Found existing collection, will add to it")
    except:
        collection = chroma_client.create_collection(name="healing_vault_books")
        print("Created new collection")
    
    # Process chunks one by one with progress
    import time
    start_time = time.time()
    
    for i, chunk in enumerate(chunks):
        # Show progress every 10 chunks
        if i % 10 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            remaining = (len(chunks) - i) / rate if rate > 0 else 0
            print(f"  Progress: {i}/{len(chunks)} chunks ({i*100//len(chunks)}%) - "
                  f"~{remaining/60:.1f} min remaining")
        
        # Generate embedding for this chunk
        try:
            embedding = embeddings.embed_query(chunk.page_content)
            
            # Add to ChromaDB
            collection.add(
                ids=[f"chunk_{i}"],
                embeddings=[embedding],
                documents=[chunk.page_content],
                metadatas=[chunk.metadata]
            )
        except Exception as e:
            print(f"  Warning: Failed to process chunk {i}: {str(e)}")
            continue
    
    print(f"\n✓ Processed all {len(chunks)} chunks in {(time.time()-start_time)/60:.1f} minutes")
    
    # Create LangChain wrapper
    vectorstore = Chroma(
        client=chroma_client,
        collection_name="healing_vault_books",
        embedding_function=embeddings
    )
    
    return vectorstore

def test_retrieval(vectorstore):
    """Test the RAG system with a sample query"""
    print("\n🔍 Testing retrieval with sample query...")
    
    query = "What does trauma do to the nervous system?"
    results = vectorstore.similarity_search(query, k=3)
    
    print(f"\nQuery: '{query}'")
    print("\nTop 3 relevant passages:\n")
    
    for i, doc in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(f"Book: {doc.metadata.get('book_title', 'Unknown')}")
        print(f"Page: {doc.metadata.get('page', 'Unknown')}")
        print(f"Content: {doc.page_content[:300]}...")
        print()

def main():
    """Main ingestion pipeline"""
    print("=" * 60)
    print("HEALING VAULT - Book Ingestion Pipeline")
    print("=" * 60)
    
    # Step 1: Load PDFs
    documents = load_pdfs(BOOKS_PATH)
    
    if not documents:
        print("❌ No documents loaded. Check your PDF path.")
        return
    
    # Step 2: Chunk documents
    chunks = chunk_documents(documents)
    
    # Step 3: Create vector database
    vectorstore = create_vectorstore(chunks)
    
    # Step 4: Test retrieval
    test_retrieval(vectorstore)
    
    print("\n✅ Ingestion complete! Your books are ready for RAG retrieval.")
    print(f"📊 Database location: {DB_PATH}")

if __name__ == "__main__":
    main()