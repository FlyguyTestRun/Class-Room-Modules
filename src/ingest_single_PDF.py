"""
Single Book RAG Ingestion for Healing Vault - INTERACTIVE VERSION
Embeds ONE book into its own isolated ChromaDB collection
Prompts user for inputs - no command-line arguments needed
"""

import os
from pathlib import Path
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama

# Configuration
EMBEDDING_MODEL = "llama3.1:8b"
LLM_MODEL = "llama3.1:8b"
DB_BASE_PATH = "./data/single_books"


def ingest_single_book():
    """Interactive book ingestion with user prompts"""
    print("=" * 70)
    print("SINGLE BOOK RAG INGESTION - INTERACTIVE MODE")
    print("=" * 70)
    
    # Step 1: Get PDF path from user
    print("\n📁 Enter the full path to your PDF:")
    print("(You can paste it directly, e.g., C:\\Users\\...\\book.pdf)")
    pdf_path = input("> ").strip().strip('"')  # Strip quotes if user copies with them
    
    # Validate PDF exists
    if not os.path.exists(pdf_path):
        print(f"\n❌ Error: PDF not found at: {pdf_path}")
        print("Make sure the path is correct and try again.")
        return
    
    # Extract book info
    book_filename = Path(pdf_path).name
    book_title = Path(pdf_path).stem
    
    print(f"\n✓ Found: {book_filename}")
    
    # Step 2: Get collection name
    print(f"\n📦 Enter a collection name (or press Enter to use: '{book_title}'):")
    print("(Use simple names like: van_der_kolk, levine, mate)")
    collection_name = input("> ").strip()
    
    if not collection_name:
        collection_name = book_title.lower().replace(" ", "_").replace("-", "_")
    
    print(f"✓ Collection name: {collection_name}")
    
    # Step 3: Determine optimal chunk size
    print(f"\n📏 Analyzing PDF to determine optimal chunk size...")
    
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        total_chars = sum(len(page.page_content) for page in pages)
        avg_chars_per_page = total_chars / len(pages) if pages else 0
        
        print(f"✓ Loaded {len(pages)} pages")
        print(f"✓ Average characters per page: {avg_chars_per_page:.0f}")
        
        # Suggest chunk size based on book characteristics
        if avg_chars_per_page > 3000:
            # Dense academic text (like van der Kolk)
            suggested_chunk = 2000
            suggested_overlap = 400
            print(f"\n💡 This appears to be dense academic text")
        elif avg_chars_per_page > 2000:
            # Standard non-fiction
            suggested_chunk = 1500
            suggested_overlap = 300
            print(f"\n💡 This appears to be standard non-fiction")
        else:
            # Lighter reading or more whitespace
            suggested_chunk = 1200
            suggested_overlap = 250
            print(f"\n💡 This appears to be lighter reading material")
        
        print(f"\n📊 Recommended settings:")
        print(f"   Chunk size: {suggested_chunk} characters (~2-3 paragraphs)")
        print(f"   Overlap: {suggested_overlap} characters (preserves context between chunks)")
        print(f"   Expected chunks: ~{total_chars // (suggested_chunk - suggested_overlap)}")
        
        print(f"\n❓ Use recommended settings? (y/n):")
        use_recommended = input("> ").strip().lower()
        
        if use_recommended == 'y' or use_recommended == '':
            chunk_size = suggested_chunk
            chunk_overlap = suggested_overlap
        else:
            print("\n📏 Enter custom chunk size (e.g., 2000):")
            chunk_size = int(input("> ").strip())
            print("📏 Enter overlap size (e.g., 400):")
            chunk_overlap = int(input("> ").strip())
    
    except Exception as e:
        print(f"⚠️  Could not analyze PDF: {e}")
        print("Using default settings: 2000 char chunks, 400 overlap")
        chunk_size = 2000
        chunk_overlap = 400
        pages = []
    
    # Add metadata
    for page in pages:
        page.metadata["book_title"] = book_title
        page.metadata["collection"] = collection_name
    
    # Step 4: Chunk documents
    print(f"\n📄 Chunking document with {chunk_size} char chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(pages)
    print(f"✓ Created {len(chunks)} chunks")
    
    # Confirm before processing
    est_time = (len(chunks) * 0.7) / 60  # Slightly slower estimate for safety
    print(f"\n⏱️  Estimated processing time: {est_time:.1f} minutes")
    print(f"\n❓ Proceed with embedding? (y/n):")
    proceed = input("> ").strip().lower()
    
    if proceed != 'y' and proceed != '':
        print("❌ Aborting ingestion")
        return
    
    # Step 5: Create embeddings and store
    print(f"\n🧠 Creating embeddings with Ollama...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    # Create database directory
    db_path = os.path.join(DB_BASE_PATH, collection_name)
    os.makedirs(db_path, exist_ok=True)
    
    # Initialize ChromaDB
    chroma_client = chromadb.PersistentClient(path=db_path)
    
    # Check if collection exists
    try:
        collection = chroma_client.get_collection(name=collection_name)
        print(f"\n⚠️  Collection '{collection_name}' already exists!")
        print(f"❓ Overwrite existing collection? (y/n):")
        overwrite = input("> ").strip().lower()
        if overwrite == 'y':
            chroma_client.delete_collection(name=collection_name)
            print("✓ Deleted existing collection")
        else:
            print("❌ Aborting to preserve existing data")
            return
    except:
        pass
    
    # Create new collection
    collection = chroma_client.create_collection(name=collection_name)
    print(f"✓ Created new collection: {collection_name}")
    
    # Process chunks with progress
    import time
    start_time = time.time()
    
    print(f"\n⏳ Processing {len(chunks)} chunks (this is the long part)...")
    for i, chunk in enumerate(chunks):
        # Show progress every 10 chunks
        if i % 10 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 and i > 0 else 0
            remaining = (len(chunks) - i) / rate if rate > 0 else 0
            progress_pct = (i * 100) // len(chunks)
            print(f"  {i}/{len(chunks)} ({progress_pct}%) - ~{remaining/60:.1f} min remaining")
        
        try:
            embedding = embeddings.embed_query(chunk.page_content)
            collection.add(
                ids=[f"{collection_name}_chunk_{i}"],
                embeddings=[embedding],
                documents=[chunk.page_content],
                metadatas=[chunk.metadata]
            )
        except Exception as e:
            print(f"  ⚠️  Chunk {i} failed: {str(e)}")
            continue
    
    elapsed_total = time.time() - start_time
    print(f"\n✓ Embedded {len(chunks)} chunks in {elapsed_total/60:.1f} minutes")
    
    # Create LangChain wrapper
    vectorstore = Chroma(
        client=chroma_client,
        collection_name=collection_name,
        embedding_function=embeddings
    )
    
    # Step 6: Test with user's own journal entry
    print(f"\n" + "=" * 70)
    print("TEST YOUR BOOK WITH A PERSONAL JOURNAL ENTRY")
    print("=" * 70)
    
    print(f"\n📝 Enter a test journal entry (or press Enter to skip):")
    print("Example: 'I was watching fireworks and flew into a blinding rage at my kid'")
    print("\n(Type your entry, then press Enter twice when done)")
    
    lines = []
    while True:
        line = input()
        if line == "" and lines:
            break
        if line:
            lines.append(line)
    
    test_entry = "\n".join(lines)
    
    if test_entry.strip():
        print(f"\n🔍 Searching book for relevant passages...")
        results = vectorstore.similarity_search(test_entry, k=3)
        
        print(f"\n📖 Top 3 Relevant Passages from {book_title}:")
        for i, doc in enumerate(results, 1):
            print(f"\n{'─' * 70}")
            print(f"PASSAGE {i}")
            print(f"Page: {doc.metadata.get('page', '?')}")
            print(f"{'─' * 70}")
            print(doc.page_content[:500] + "...")
        
        # Optional: Generate AI response
        print(f"\n❓ Generate AI response based on these passages? (y/n):")
        gen_response = input("> ").strip().lower()
        
        if gen_response == 'y':
            print(f"\n🧠 Generating response...")
            
            context = "\n\n".join([
                f"From page {doc.metadata.get('page', '?')}:\n{doc.page_content[:600]}"
                for doc in results
            ])
            
            llm = Ollama(model=LLM_MODEL, temperature=0.7)
            
            prompt = f"""You are a trauma specialist who deeply understands The Body Keeps the Score by Bessel van der Kolk.

Journal Entry:
"{test_entry}"

Relevant passages from the book:
{context}

Respond in 4-6 sentences. Reference van der Kolk's insights naturally. Be compassionate and somatic-focused."""
            
            response = llm.invoke(prompt)
            
            print(f"\n{'═' * 70}")
            print("TRAUMA SPECIALIST RESPONSE:")
            print(f"{'═' * 70}")
            print(response)
            print(f"{'═' * 70}")
    
    # Summary
    print(f"\n" + "=" * 70)
    print("✅ INGESTION COMPLETE!")
    print("=" * 70)
    print(f"📚 Book: {book_title}")
    print(f"📦 Collection: {collection_name}")
    print(f"📊 Database: {db_path}")
    print(f"📈 Total chunks: {len(chunks)}")
    print(f"⏱️  Processing time: {elapsed_total/60:.1f} minutes")
    print("=" * 70)


if __name__ == "__main__":
    ingest_single_book()