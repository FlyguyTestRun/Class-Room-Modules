import chromadb

DB_PATH = "./data/chroma_db"

try:
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection("healing_vault_books")
    count = collection.count()
    
    print(f"✓ Database found!")
    print(f"✓ Collection 'healing_vault_books' exists")
    print(f"✓ Number of embedded chunks: {count}")
    
    if count > 0:
        print(f"\n✅ Database is healthy with {count} chunks")
    else:
        print(f"\n❌ Database is empty (0 chunks)")
        
except Exception as e:
    print(f"❌ Database error: {e}")