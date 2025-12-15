"""
Trauma Specialist - Somatic Trauma Guide
Integrates insights from van der Kolk, Levine, and Maté
"""

import os
import chromadb
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama

# Configuration
EMBEDDING_MODEL = "llama3.1:8b"
LLM_MODEL = "llama3.1:8b"
DB_BASE_PATH = "./data/single_books"

# Trauma books to search
TRAUMA_COLLECTIONS = {
    "van_der_kolk": r"C:\Users\GameRoom PC Shaw1\OneDrive\Desktop\healing-vault\data\single_books\Van_Der_Kolk_Body-Keeps-Score",  # Corrected path
    "levine": r"C:\Users\GameRoom PC Shaw1\OneDrive\Desktop\healing-vault\data\single_books\waking_the_tiger___peter_levine",  # Corrected path
    "mate": r"C:\Users\GameRoom PC Shaw1\OneDrive\Desktop\healing-vault\data\single_books\the_myth_of_normal_by_gabor_mate"  # Corrected path
}


class TraumaSpecialist:
    """Somatic trauma therapist integrating three trauma experts"""
    
    def __init__(self):
        """Initialize with access to all three trauma books"""
        print("🛡️ Initializing Trauma Specialist...")
        
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        self.llm = Ollama(model=LLM_MODEL, temperature=0.7)
        
        # Load all three trauma collections
        self.collections = {}
        
        for author, path in TRAUMA_COLLECTIONS.items():
            full_path = os.path.join(DB_BASE_PATH, path)
            
            if not os.path.exists(full_path):
                print(f"⚠️  {author} collection not found at {full_path}")
                continue
            
            try:
                collection_name = Path(path).name
                chroma_client = chromadb.PersistentClient(path=full_path)
                
                vectorstore = Chroma(
                    client=chroma_client,
                    collection_name=collection_name,
                    embedding_function=self.embeddings
                )
                
                self.collections[author] = {
                    "vectorstore": vectorstore,
                    "name": collection_name
                }
                
                print(f"✓ Loaded {author}")
            
            except Exception as e:
                print(f"⚠️  Failed to load {author}: {e}")
        
        if not self.collections:
            raise Exception("No trauma collections loaded. Check your collection paths.")
        
        print(f"✓ Trauma Specialist ready with {len(self.collections)} book(s)\n")
    
    def search_all_trauma_books(self, query, k=2):
        """
        Search across all trauma books and return most relevant passages
        
        Args:
            query: User's journal entry
            k: Number of results per book
            
        Returns:
            List of (author, document) tuples
        """
        results = []
        
        for author, coll_data in self.collections.items():
            vectorstore = coll_data["vectorstore"]
            
            try:
                docs = vectorstore.similarity_search(query, k=k)
                for doc in docs:
                    results.append((author, doc))
            except Exception as e:
                print(f"⚠️  Search failed for {author}: {e}")
        
        return results
    
    def respond(self, journal_entry):
        """
        Generate trauma specialist response to journal entry
        
        Args:
            journal_entry: User's text
            
        Returns:
            Specialist's response with book citations
        """
        print(f"🔍 Searching trauma library...")
        
        # Search all three books
        results = self.search_all_trauma_books(journal_entry, k=2)
        
        if not results:
            return "I couldn't find relevant passages. Please check your trauma book collections."
        
        print(f"✓ Found {len(results)} relevant passages\n")
        
        # Build context from all three authors
        context_parts = []
        
        for author, doc in results:
            page = doc.metadata.get('page', '?')
            preview = doc.page_content[:400]
            
            context_parts.append(f"From {author} (page {page}):\n{preview}")
        
        context = "\n\n".join(context_parts)
        
        # Build prompt
        system_prompt = """You are a Trauma & Nervous System Specialist who integrates insights from three masters:

**Bessel van der Kolk (The Body Keeps the Score):**
- Trauma is stored in the body, not just memory
- The nervous system holds the score
- Freeze/immobilization is protective, not weakness
- Treatments: EMDR, neurofeedback, body-based therapies

**Peter Levine (Waking the Tiger):**
- Trauma is incomplete survival responses
- Titration: Small, manageable doses of activation
- Pendulation: Oscillating between activation and calm
- Discharge: Releasing trapped energy through gentle movement

**Gabor Maté (The Myth of Normal):**
- Trauma is disconnection from self
- Compassionate inquiry: What happened TO you, not what's wrong WITH you
- Self-compassion is essential for healing
- Relational trauma needs relational healing

**Your voice:**
- Somatic and body-focused ("Your body is speaking...")
- Normalize trauma responses (not pathologize)
- Name nervous system states (freeze, hyperarousal, shutdown)
- Offer gentle next steps, not fixing

**Guidelines:**
- Respond in 4-6 sentences ONLY
- Reference authors naturally (e.g., "Van der Kolk describes this as...")
- Do NOT quote full paragraphs (copyright violation)
- Synthesize insights, don't just list them
- Be compassionate but direct

DO NOT diagnose. DO validate their nervous system's response."""

        user_prompt = f"""Journal Entry:
"{journal_entry}"

Relevant passages from trauma experts:
{context}

Respond as the Trauma Specialist, integrating insights from all three authors where relevant."""

        print("🧠 Generating response...\n")
        
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = self.llm.invoke(full_prompt)
        
        return response.strip()
    
    def show_sources(self, journal_entry):
        """Show which passages were used for the response"""
        results = self.search_all_trauma_books(journal_entry, k=2)
        
        print("📚 SOURCE PASSAGES USED:\n")
        
        for i, (author, doc) in enumerate(results, 1):
            print(f"{'─' * 70}")
            print(f"{i}. {author.upper()} - Page {doc.metadata.get('page', '?')}")
            print(f"{'─' * 70}")
            print(doc.page_content[:500] + "...")
            print()


def test_trauma_specialist():
    """Test the trauma specialist with sample entries"""
    
    specialist = TraumaSpecialist()
    
    test_entries = [
        {
            "name": "Fireworks Rage",
            "text": """I was watching fireworks with my family and suddenly flew into a blinding rage at my kid for making noise. I couldn't control it—my body just took over. Afterward I felt horrible and ashamed. Why do I react like this?"""
        },
        {
            "name": "Freeze Response",
            "text": """My boss raised his voice in a meeting and I completely froze. I couldn't speak, couldn't move, chest got tight. Everyone else seemed fine but I was panicking inside. I hate being this weak."""
        },
        {
            "name": "Childhood Pattern",
            "text": """I keep dating emotionally unavailable people. My therapist says it's because my dad was never there emotionally. But I don't understand how childhood stuff affects me now as an adult. I thought I dealt with that already."""
        }
    ]
    
    for entry in test_entries:
        print("=" * 70)
        print(f"TEST: {entry['name']}")
        print("=" * 70)
        print(f"\nJOURNAL ENTRY:\n{entry['text']}\n")
        
        # Get response
        response = specialist.respond(entry['text'])
        
        print("=" * 70)
        print("TRAUMA SPECIALIST RESPONSE:")
        print("=" * 70)
        print(response)
        print("\n")
        
        # Show sources
        specialist.show_sources(entry['text'])
        
        print("\n" + "=" * 70 + "\n")
        
        # Pause between entries
        input("Press Enter for next entry...")


if __name__ == "__main__":
    from pathlib import Path
    test_trauma_specialist()