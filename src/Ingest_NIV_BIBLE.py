"""
PDF Ingestion Pipeline for Healing Vault - NIV BIBLE PDF VERSION (ALL REQUESTED BOOKS)
Processes the NIV Bible PDF into ChromaDB for RAG retrieval, including ALL the books you listed
"""

import os
from pathlib import Path
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import time
import re

# ==================== CONFIGURATION ====================
# Path to your NIV Bible PDF
SINGLE_PDF_PATH = r"C:\Users\GameRoom PC Shaw1\OneDrive\Desktop\Psycology Books\NIV-Bible.pdf"

DB_PATH = "./data/chroma_db_niv_bible_full_list"  # New DB for this expanded list
EMBEDDING_MODEL = "nomic-embed-text"              # Fast, high-quality embeddings

# ALL THE BOOKS YOU WANT TO INCLUDE (expanded list – everything you specified)
INCLUDED_BOOKS = {
    # Old Testament
    "Genesis", "Exodus", "Leviticus", "Joshua", "Judges", "Ruth",
    "1 Samuel", "2 Samuel", "Ezra", "Nehemiah", "Esther",
    "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Lamentations", "Ezekiel", "Daniel",
    "Hosea", "Jonah", "Micah", "Habakkuk", "Zechariah", "Malachi",
    
    # New Testament
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians",
    "1 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon",
    "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John"
}

# Normalize common variations in PDF formatting
BOOK_NORMALIZATION = {
    "Song of Songs": "Song of Solomon",
    "Songs": "Song of Solomon",
    "1Samuel": "1 Samuel",
    "2Samuel": "2 Samuel",
    "1Thessalonians": "1 Thessalonians",
    # Add more if you see mismatches during the first run
}

# Common book header patterns in NIV PDFs
BOOK_PATTERNS = [
    r'^THE BOOK OF (\w+)',           # "THE BOOK OF GENESIS"
    r'^Book of (\w+)',               # "Book of Exodus"
    r'^(\w+)\s+Chapter\s+\d+',       # "Genesis Chapter 1"
    r'^(\w+)\s+\d+:\d+',             # "Genesis 1:1"
    r'^(\w+)\s+1$',                  # "Genesis 1"
]

# ======================================================

def load_single_pdf(pdf_path):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return []
    
    print(f"📚 Loading NIV Bible PDF: {pdf_path.name}")
    try:
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        for page in pages:
            page.metadata["source_file"] = pdf_path.name
            page.metadata["book_title"] = pdf_path.stem
        print(f"✓ Loaded {len(pages)} pages")
        return pages
    except Exception as e:
        print(f"✗ Error loading PDF: {str(e)}")
        return []

def detect_bible_book(text):
    for pattern in BOOK_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            book = match.group(1).strip().title()
            return BOOK_NORMALIZATION.get(book, book)
    return None

def chunk_documents(documents):
    print("\n📄 Chunking document with book detection...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,   # ~200-300 words – excellent for verse-level retrieval
        chunk_overlap=200, # Preserves context across chapter/verse boundaries
        length_function=len,
    )
    
    current_book = "Unknown"
    all_chunks = []
    
    for doc in documents:
        page_text = doc.page_content
        detected = detect_bible_book(page_text)
        if detected:
            current_book = detected
            print(f"Detected book: {current_book} (page {doc.metadata.get('page', '?')})")
        
        doc.metadata["bible_book"] = current_book
        chunks = text_splitter.split_documents([doc])
        all_chunks.extend(chunks)
    
    print(f"✓ Created {len(all_chunks)} chunks")
    return all_chunks

def create_vectorstore(chunks):
    print("\n🧠 Generating embeddings – INCLUDING ALL YOUR REQUESTED BOOKS...")
    print(f"⏳ Processing chunks (skipping anything outside the list)...\n")
    
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    os.makedirs(DB_PATH, exist_ok=True)
    
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    try:
        collection = chroma_client.get_collection(name="healing_vault_niv_bible_full")
        print("Found existing collection – will add to it")
    except:
        collection = chroma_client.create_collection(name="healing_vault_niv_bible_full")
        print("Created new collection")
    
    start_time = time.time()
    added = 0
    skipped = 0
    
    for i, chunk in enumerate(chunks):
        if i % 10 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            remaining = (len(chunks) - i) / rate if rate > 0 else 0
            print(f"  Progress: {i}/{len(chunks)} ({i*100//len(chunks)}%) – ~{remaining/60:.1f} min left")
        
        bible_book = chunk.metadata.get("bible_book", "Unknown")
        
        if bible_book not in INCLUDED_BOOKS:
            skipped += 1
            continue
        
        try:
            embedding = embeddings.embed_query(chunk.page_content)
            collection.add(
                ids=[f"chunk_{i}"],
                embeddings=[embedding],
                documents=[chunk.page_content],
                metadatas=[chunk.metadata]
            )
            added += 1
        except Exception as e:
            print(f"  Warning: Failed chunk {i}: {e}")
    
    print(f"\n✓ Ingestion complete in {(time.time()-start_time)/60:.1f} minutes")
    print(f"Added {added} chunks | Skipped {skipped} chunks (outside your requested list)")
    
    vectorstore = Chroma(
        client=chroma_client,
        collection_name="healing_vault_niv_bible_full",
        embedding_function=embeddings
    )
    return vectorstore

def test_retrieval(vectorstore):
    print("\n🔍 Testing retrieval on your full NIV list...")
    queries = [
        "Paul's teaching on grace and the renewal of the mind",
        "David's prayers of repentance and restoration in the Psalms",
        "John's description of God's love casting out fear",
        "James on faith demonstrated by works"
    ]
    for query in queries:
        print(f"\nQuery: {query}")
        results = vectorstore.similarity_search(query, k=3)
        for j, doc in enumerate(results, 1):
            book = doc.metadata.get("bible_book", "Unknown")
            print(f"  [{j}] {book}")
            print(f"      {doc.page_content[:250]}...\n")

def main():
    print("=" * 70)
    print("HEALING VAULT - NIV Bible Ingestion (All Requested Books)")
    print("=" * 70)
    
    documents = load_single_pdf(SINGLE_PDF_PATH)
    if not documents:
        return
    
    chunks = chunk_documents(documents)
    vectorstore = create_vectorstore(chunks)
    test_retrieval(vectorstore)
    
    print(f"\n✅ Database ready! All your requested NIV books are embedded.")
    print(f"📂 Saved at: {DB_PATH}")

if __name__ == "__main__":
    main()