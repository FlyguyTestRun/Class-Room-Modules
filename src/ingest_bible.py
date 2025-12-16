"""
Healing Vault — Automated Bible Ingestion Pipeline
=================================================

Purpose:
--------
• Ingest multiple Bible PDFs (KJV, NIV, etc.)
• Detect biblical book boundaries automatically
• Route chunks into author-isolated ChromaDB collections
• Preserve trauma-safe, non-preachy retrieval architecture

Design Principles:
------------------
• No future code edits when adding authors or PDFs
• One vector store per author (Paul ≠ Peter)
• Clear, annotated structure for future expansion
"""

# =====================================================
# IMPORTS
# =====================================================

import os
import time
import re
from pathlib import Path
import chromadb

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from biblical_persona import BIBLICAL_VOICES


# =====================================================
# CONFIGURATION
# =====================================================

# Folder containing all Bible PDFs (KJV, NIV, future translations)
BIBLE_PDF_DIR = r"C:\Users\GameRoom PC Shaw1\OneDrive\Desktop\Psycology Books\Spiritual & Relational"

# Base directory where author-specific vector DBs will be stored
RAG_BASE_PATH = "./rag/bible"

# Embedding model (fast, local, stable)
EMBEDDING_MODEL = "nomic-embed-text"


# =====================================================
# BUILD AUTHOR → BOOK MAP (AUTOMATED)
# =====================================================
"""
Creates a lookup table such that:
    "romans" → "paul"
    "john"   → "john"

This is the *single source of truth* for routing.
Adding a new author only requires updating biblical_persona.py
"""

BOOK_TO_AUTHOR = {}

for persona_key, persona in BIBLICAL_VOICES.items():
    for book in persona.get("books_authored", []):
        BOOK_TO_AUTHOR[book.lower()] = persona_key

INCLUDED_BOOKS = set(book.title() for book in BOOK_TO_AUTHOR.keys())


# =====================================================
# BOOK NORMALIZATION & DETECTION
# =====================================================
"""
Handles formatting differences across Bible translations.
"""

BOOK_NORMALIZATION = {
    "Song of Songs": "Song of Solomon",
    "Songs": "Song of Solomon",
    "1Samuel": "1 Samuel",
    "2Samuel": "2 Samuel",
}

BOOK_PATTERNS = [
    r'The Book of ([A-Za-z ]+)',
    r'Book of ([A-Za-z ]+)',
    r'^([1-3]?\s?[A-Za-z]+)\s+Chapter\s+1',
    r'^([1-3]?\s?[A-Za-z]+)\s+\d+:\d+',
    r'^THE BOOK OF ([A-Z ]+)',
]


# =====================================================
# LOAD ALL BIBLE PDFs
# =====================================================

def load_all_bible_pdfs(pdf_dir: str):
    """
    Loads every PDF in the specified directory.
    Each page retains source metadata.
    """
    pdf_dir = Path(pdf_dir)
    if not pdf_dir.exists():
        print(f"❌ PDF directory not found: {pdf_dir}")
        return []

    documents = []

    for pdf_path in pdf_dir.glob("*.pdf"):
        print(f"\n📚 Loading {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()

        for page in pages:
            page.metadata["source_file"] = pdf_path.name

        print(f"✓ Loaded {len(pages)} pages")
        documents.extend(pages)

    return documents


# =====================================================
# INFER BOOK NAME FROM TEXT
# =====================================================

def detect_bible_book(text: str) -> str | None:
    """
    Uses regex patterns to infer the biblical book
    from raw text content.
    """
    for pattern in BOOK_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            book = match.group(1).strip().title()
            return BOOK_NORMALIZATION.get(book, book)
    return None


# =====================================================
# CHUNK DOCUMENTS WITH BOOK CONTEXT
# =====================================================

def chunk_documents(documents):
    """
    Splits documents into overlapping chunks
    while preserving detected book context.
    """
    print("\n📄 Chunking documents with book detection...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,      # ~10–15 verses
        chunk_overlap=200,    # preserves narrative flow
        length_function=len,
    )

    current_book = "Unknown"
    chunks = []

    for doc in documents:
        detected = detect_bible_book(doc.page_content)
        if detected:
            current_book = detected
            print(f"Detected book: {current_book}")

        doc.metadata["bible_book"] = current_book
        chunks.extend(splitter.split_documents([doc]))

    print(f"✓ Created {len(chunks)} chunks")
    return chunks


# =====================================================
# INGEST PIPELINE — AUTHOR ISOLATED
# =====================================================

def ingest_by_author(chunks):
    """
    Routes chunks into one ChromaDB collection per author.
    Prevents cross-author semantic bleed.
    """
    print("\n🧠 Ingesting into author-specific vector stores...\n")

    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    os.makedirs(RAG_BASE_PATH, exist_ok=True)

    author_buffers = {}

    for chunk in chunks:
        book = chunk.metadata.get("bible_book", "").lower()
        if book not in BOOK_TO_AUTHOR:
            continue

        author = BOOK_TO_AUTHOR[book]

        chunk.metadata.update({
            "book": book,
            "author": author,
            "source": "bible",
        })

        author_buffers.setdefault(author, []).append(chunk)

    for author, author_chunks in author_buffers.items():
        author_path = Path(RAG_BASE_PATH) / author
        author_path.mkdir(parents=True, exist_ok=True)

        print(f"📚 {author.upper()} — {len(author_chunks)} chunks")

        Chroma.from_documents(
            documents=author_chunks,
            embedding=embeddings,
            persist_directory=str(author_path),
            collection_name=author
        )

    print("\n✅ Author-based ingestion complete.")


# =====================================================
# RETRIEVAL SANITY CHECK
# =====================================================

def test_retrieval():
    """
    Confirms isolation and relevance per author.
    """
    print("\n🔍 Testing author-isolated retrieval...\n")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    tests = {
        "paul": "grace and forgiveness",
        "john": "love and abiding",
        "david": "repentance and restoration",
        "james": "faith and works"
    }

    for author, query in tests.items():
        path = Path(RAG_BASE_PATH) / author
        if not path.exists():
            continue

        vs = Chroma(
            persist_directory=str(path),
            embedding_function=embeddings,
            collection_name=author
        )

        print(f"\n[{author.upper()}] Query: {query}")
        results = vs.similarity_search(query, k=2)
        for r in results:
            print(f"  • {r.metadata.get('book')} — {r.page_content[:200]}...\n")


# =====================================================
# MAIN ENTRY POINT
# =====================================================

def main():
    print("=" * 70)
    print("HEALING VAULT — Author-Based Bible RAG Ingestion")
    print("=" * 70)

    documents = load_all_bible_pdfs(BIBLE_PDF_DIR)
    if not documents:
        return

    chunks = chunk_documents(documents)
    ingest_by_author(chunks)
    test_retrieval()

    print("\n📂 Vector stores saved to:", RAG_BASE_PATH)
    print("✅ Ready for RAG controller integration.")


if __name__ == "__main__":
    main()
