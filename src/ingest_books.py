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
BOOKS_PATH = r"C:\Users\Bryan\OneDrive\Desktop\Psycology Books\Core Books"  # Your PDF folder
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
    """Create embeddings and store in ChromaDB"""
    print("\n🧠 Creating embeddings with Ollama...")
    print(f"⏳ Processing {len(chunks)} chunks (this may take 20-45 minutes)...")
    
    # Initialize Ollama embeddings
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    # Create vector database
    os.makedirs(DB_PATH, exist_ok=True)
    
    # Process in batches with progress tracking
    batch_size = 50
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    
    print(f"Processing in {total_batches} batches of {batch_size} chunks each...")
    
    vectorstore = None
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        print(f"  Batch {batch_num}/{total_batches} ({i}/{len(chunks)} chunks) - Processing...")
        
        if vectorstore is None:
            # Create initial vectorstore
            vectorstore = Chroma.from_documents(
                documents=batch,
                embedding=embeddings,
                persist_directory=DB_PATH
            )
        else:
            # Add to existing vectorstore
            vectorstore.add_documents(batch)
        
        print(f"  ✓ Batch {batch_num}/{total_batches} complete")
    
    print(f"✓ Vector database created at {DB_PATH}")
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