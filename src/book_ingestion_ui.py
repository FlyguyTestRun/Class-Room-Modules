"""
Universal Document Ingestion System - Healing Vault
Batch embedding with intelligent organization and per-document optimization
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
import time
import json

# Configuration
EMBEDDING_MODEL = "llama3.1:8b"
LLM_MODEL = "llama3.1:8b"
DB_BASE_PATH = "./data/single_books"
SETTINGS_FILE = "./data/.ingestion_settings.json"

# Initialize session state
if 'last_folder' not in st.session_state:
    st.session_state.last_folder = ""
if 'last_chunk_size' not in st.session_state:
    st.session_state.last_chunk_size = 2000
if 'last_overlap' not in st.session_state:
    st.session_state.last_overlap = 400

# Page config
st.set_page_config(
    page_title="Document Ingestion System",
    page_icon="🗂️",
    layout="wide"
)

st.title("🗂️ Universal Document Ingestion System")
st.markdown("Embed any documents into organized, searchable collections")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Tab selection
    tab = st.radio("View", ["📤 Ingest", "📚 Browse Collections"], label_visibility="collapsed")

# Main content
if tab == "📤 Ingest":
    
    # File upload
    uploaded_files = st.file_uploader(
        "📁 Upload Documents (Multiple PDFs Supported)",
        type=['pdf'],
        accept_multiple_files=True,
        help="Drag and drop multiple PDFs to process them sequentially"
    )
    
    if uploaded_files:
        st.success(f"✓ {len(uploaded_files)} document(s) loaded")
        
        # Show file list
        with st.expander("📋 Uploaded Files", expanded=True):
            for i, file in enumerate(uploaded_files, 1):
                file_size_mb = file.size / 1024 / 1024
                st.text(f"{i}. {file.name} ({file_size_mb:.1f} MB)")
        
        st.markdown("---")
        
        # Organization section
        st.subheader("📁 Organization")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Get existing folders
            existing_folders = []
            if os.path.exists(DB_BASE_PATH):
                for item in os.listdir(DB_BASE_PATH):
                    item_path = os.path.join(DB_BASE_PATH, item)
                    if os.path.isdir(item_path):
                        existing_folders.append(item)
            
            # Folder selection
            folder_options = ["[Root - No Folder]"] + existing_folders + ["[Create New Folder]"]
            
            folder_choice = st.selectbox(
                "Topic Folder",
                options=folder_options,
                index=folder_options.index(st.session_state.last_folder) if st.session_state.last_folder in folder_options else 0,
                help="Group related documents together"
            )
            
            # Handle new folder creation
            if folder_choice == "[Create New Folder]":
                new_folder = st.text_input(
                    "New folder name",
                    placeholder="e.g., trauma, attachment, biblical",
                    help="Use lowercase, no spaces or special characters"
                )
                folder_group = new_folder if new_folder else None
            elif folder_choice == "[Root - No Folder]":
                folder_group = None
            else:
                folder_group = folder_choice
        
        with col2:
            if existing_folders:
                st.markdown("**Existing:**")
                for folder in existing_folders:
                    st.text(f"📁 {folder}")
        
        # Preview structure
        if folder_group:
            st.info(f"📂 Documents will be stored in: `{DB_BASE_PATH}/{folder_group}/[collection]/`")
        else:
            st.info(f"📂 Documents will be stored in: `{DB_BASE_PATH}/[collection]/`")
        
        st.markdown("---")
        
        # Processing options
        st.subheader("⚙️ Processing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            auto_name = st.checkbox("Auto-generate collection names", value=True, help="Use filename as collection name")
            per_doc_analysis = st.checkbox("Analyze each document individually", value=True, help="Optimize chunk size per document")
        
        # Initialize defaults
        default_chunk = st.session_state.last_chunk_size
        default_overlap = st.session_state.last_overlap
        
        with col2:
            if not per_doc_analysis:
                st.markdown("**Default Settings:**")
                default_chunk = st.number_input("Chunk Size", 1000, 3000, st.session_state.last_chunk_size, 100)
                default_overlap = st.number_input("Overlap", 100, 500, st.session_state.last_overlap, 50)
        
        # Collection name preview
        if auto_name:
            with st.expander("🏷️ Auto-Generated Names"):
                for file in uploaded_files:
                    suggested_name = Path(file.name).stem.lower().replace(" ", "_").replace("-", "_")[:50]
                    st.code(f"{file.name} → {suggested_name}")
        
        st.markdown("---")
        
        # Process button
        if st.button("🚀 Process All Documents", type="primary", use_container_width=True):
            
            # Save last settings
            st.session_state.last_folder = folder_choice
            if not per_doc_analysis:
                st.session_state.last_chunk_size = default_chunk
                st.session_state.last_overlap = default_overlap
            
            # Overall progress
            overall_progress = st.progress(0)
            overall_status = st.empty()
            
            # Results tracking
            results = {
                "success": [],
                "failed": [],
                "total_chunks": 0,
                "total_time": 0
            }
            
            batch_start = time.time()
            
            # Process each file
            for file_idx, uploaded_file in enumerate(uploaded_files):
                
                overall_status.markdown(f"### 📄 Document {file_idx + 1}/{len(uploaded_files)}: {uploaded_file.name}")
                
                # Save file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    pdf_path = tmp_file.name
                
                try:
                    # Step 1: Load and analyze
                    with st.spinner("Loading document..."):
                        loader = PyPDFLoader(pdf_path)
                        pages = loader.load()
                    
                    st.text(f"✓ Loaded {len(pages)} pages")
                    
                    # Per-document analysis
                    if per_doc_analysis:
                        total_chars = sum(len(page.page_content) for page in pages)
                        avg_chars_per_page = total_chars / len(pages) if pages else 0
                        
                        # Smart chunk sizing
                        if avg_chars_per_page > 3000:
                            chunk_size, chunk_overlap = 2000, 400
                            doc_type = "Dense academic text"
                        elif avg_chars_per_page > 2000:
                            chunk_size, chunk_overlap = 1500, 300
                            doc_type = "Standard document"
                        else:
                            chunk_size, chunk_overlap = 1200, 250
                            doc_type = "Light reading"
                        
                        st.info(f"""
                        **Analysis:** {doc_type}
                        - Avg chars/page: {avg_chars_per_page:.0f}
                        - Chunk size: {chunk_size}
                        - Overlap: {chunk_overlap}
                        """)
                        
                        # Allow override
                        with st.expander("⚙️ Override Settings"):
                            col1, col2 = st.columns(2)
                            with col1:
                                chunk_size = st.number_input(
                                    "Chunk Size",
                                    1000, 3000, chunk_size, 100,
                                    key=f"chunk_{file_idx}"
                                )
                            with col2:
                                chunk_overlap = st.number_input(
                                    "Overlap",
                                    100, 500, chunk_overlap, 50,
                                    key=f"overlap_{file_idx}"
                                )
                    else:
                        chunk_size = default_chunk
                        chunk_overlap = default_overlap
                    
                    # Collection name
                    if auto_name:
                        collection_name = Path(uploaded_file.name).stem.lower().replace(" ", "_").replace("-", "_")[:50]
                    else:
                        collection_name = st.text_input(
                            f"Collection name",
                            value=Path(uploaded_file.name).stem.lower().replace(" ", "_").replace("-", "_")[:50],
                            key=f"coll_{file_idx}"
                        )
                    
                    # Add metadata
                    doc_title = Path(uploaded_file.name).stem
                    for page in pages:
                        page.metadata["document_title"] = doc_title
                        page.metadata["collection"] = collection_name
                        page.metadata["original_filename"] = uploaded_file.name
                        if folder_group:
                            page.metadata["topic_folder"] = folder_group
                    
                    # Step 2: Chunk
                    with st.spinner("Chunking document..."):
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=chunk_size,
                            chunk_overlap=chunk_overlap,
                            length_function=len,
                        )
                        chunks = text_splitter.split_documents(pages)
                    
                    st.text(f"✓ Created {len(chunks)} chunks")
                    
                    # Step 3: Embed
                    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
                    
                    # Setup database path
                    if folder_group:
                        db_path = os.path.join(DB_BASE_PATH, folder_group, collection_name)
                    else:
                        db_path = os.path.join(DB_BASE_PATH, collection_name)
                    
                    os.makedirs(db_path, exist_ok=True)
                    
                    chroma_client = chromadb.PersistentClient(path=db_path)
                    
                    # Delete existing
                    try:
                        chroma_client.delete_collection(name=collection_name)
                    except:
                        pass
                    
                    collection = chroma_client.create_collection(name=collection_name)
                    
                    # Process chunks
                    file_progress = st.progress(0)
                    file_status = st.empty()
                    file_start = time.time()
                    
                    for i, chunk in enumerate(chunks):
                        try:
                            embedding = embeddings.embed_query(chunk.page_content)
                            collection.add(
                                ids=[f"{collection_name}_chunk_{i}"],
                                embeddings=[embedding],
                                documents=[chunk.page_content],
                                metadatas=[chunk.metadata]
                            )
                            
                            # Progress
                            file_progress.progress((i + 1) / len(chunks))
                            
                            if i % 10 == 0:
                                elapsed = time.time() - file_start
                                rate = i / elapsed if elapsed > 0 and i > 0 else 0
                                remaining = (len(chunks) - i) / rate if rate > 0 else 0
                                file_status.text(f"🧠 {i}/{len(chunks)} chunks (~{remaining/60:.1f} min)")
                        
                        except Exception as e:
                            st.warning(f"Chunk {i} failed: {str(e)}")
                            continue
                    
                    file_time = time.time() - file_start
                    file_status.text("✅ Complete!")
                    
                    # Record success
                    results["success"].append({
                        "name": uploaded_file.name,
                        "collection": collection_name,
                        "chunks": len(chunks),
                        "time": file_time,
                        "path": db_path
                    })
                    results["total_chunks"] += len(chunks)
                    
                    st.success(f"✅ {uploaded_file.name}: {len(chunks)} chunks in {file_time/60:.1f} min")
                
                except Exception as e:
                    st.error(f"❌ {uploaded_file.name}: {str(e)}")
                    results["failed"].append({"name": uploaded_file.name, "error": str(e)})
                
                finally:
                    if os.path.exists(pdf_path):
                        os.unlink(pdf_path)
                
                # Update overall
                overall_progress.progress((file_idx + 1) / len(uploaded_files))
                st.markdown("---")
            
            # Summary
            results["total_time"] = time.time() - batch_start
            
            st.markdown("## 📊 Batch Complete")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("✅ Success", len(results["success"]))
            with col2:
                st.metric("❌ Failed", len(results["failed"]))
            with col3:
                st.metric("📦 Total Chunks", results["total_chunks"])
            with col4:
                st.metric("⏱️ Time", f"{results['total_time']/60:.1f} min")
            
            if results["success"]:
                with st.expander("✅ Successfully Embedded", expanded=True):
                    for item in results["success"]:
                        st.markdown(f"**{item['name']}** → `{item['collection']}` ({item['chunks']} chunks, {item['time']/60:.1f} min)")
    
    else:
        st.info("👆 Upload PDFs to begin")

elif tab == "📚 Browse Collections":
    st.subheader("📚 Collection Browser")
    
    if not os.path.exists(DB_BASE_PATH):
        st.warning("No collections found. Upload documents first.")
    else:
        # Build tree structure
        tree = {}
        for root, dirs, files in os.walk(DB_BASE_PATH):
            if any(f.endswith('.sqlite3') for f in files):
                rel_path = os.path.relpath(root, DB_BASE_PATH)
                parts = rel_path.split(os.sep)
                
                if len(parts) == 1:
                    # Root level collection
                    if "root" not in tree:
                        tree["root"] = []
                    tree["root"].append(parts[0])
                else:
                    # Folder collection
                    folder = parts[0]
                    collection = parts[1]
                    if folder not in tree:
                        tree[folder] = []
                    tree[folder].append(collection)
        
        # Display tree
        for folder, collections in sorted(tree.items()):
            if folder == "root":
                st.markdown("### 📁 Root Collections")
            else:
                st.markdown(f"### 📁 {folder.upper()}")
            
            for coll in sorted(collections):
                st.text(f"  📘 {coll}")
        
        # Test interface
        st.markdown("---")
        st.subheader("🧪 Test a Collection")
        
        all_collections = [(f, c) for f, colls in tree.items() for c in colls]
        
        if all_collections:
            selected = st.selectbox(
                "Select collection",
                options=[f"{f}/{c}" if f != "root" else c for f, c in all_collections]
            )
            
            test_query = st.text_area("Test query", placeholder="Enter text to search...")
            
            if st.button("🔍 Search") and test_query:
                # Parse selection
                if "/" in selected:
                    folder, coll = selected.split("/")
                    db_path = os.path.join(DB_BASE_PATH, folder, coll)
                else:
                    coll = selected
                    db_path = os.path.join(DB_BASE_PATH, coll)
                
                with st.spinner("Searching..."):
                    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
                    chroma_client = chromadb.PersistentClient(path=db_path)
                    vectorstore = Chroma(
                        client=chroma_client,
                        collection_name=coll,
                        embedding_function=embeddings
                    )
                    
                    results = vectorstore.similarity_search(test_query, k=3)
                
                st.markdown("### 📖 Top 3 Results")
                for i, doc in enumerate(results, 1):
                    with st.expander(f"Result {i} - Page {doc.metadata.get('page', '?')}"):
                        st.write(doc.page_content[:600])