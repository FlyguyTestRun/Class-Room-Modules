"""
Silent Scribe - Memory & Context Manager
Stores intake, tracks characters, identifies patterns
Never speaks - only remembers and provides context to other agents
"""

import json
import os
from datetime import datetime
from pathlib import Path
import chromadb
from langchain_community.embeddings import OllamaEmbeddings

SILENT_SCRIBE_PATH = "./data/silent_scribe"
EMBEDDING_MODEL = "llama3.1:8b"


class SilentScribe:
    """The memory keeper - tracks everything, speaks to no one"""
    
    def __init__(self):
        """Initialize Silent Scribe memory system"""
        os.makedirs(SILENT_SCRIBE_PATH, exist_ok=True)
        
        self.intake_file = os.path.join(SILENT_SCRIBE_PATH, "intake.json")
        self.characters_file = os.path.join(SILENT_SCRIBE_PATH, "characters.json")
        self.entries_file = os.path.join(SILENT_SCRIBE_PATH, "journal_entries.json")
        
        # Load existing data
        self.intake = self._load_json(self.intake_file)
        self.characters = self._load_json(self.characters_file, default={"characters": {}})
        self.entries = self._load_json(self.entries_file, default={"entries": []})
        
        # Setup ChromaDB
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        self.chroma_client = chromadb.PersistentClient(path=SILENT_SCRIBE_PATH)
    
    def _load_json(self, filepath, default=None):
        """Load JSON file or return default"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath, data):
        """Save data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_intake_context(self):
        """Get user's initial intake story for agent context"""
        if not self.intake:
            return "No intake information available."
        
        context = f"""
USER BACKGROUND (from intake):
- Story: {self.intake.get('story', 'N/A')}
- Current Struggle: {self.intake.get('current_struggle', 'N/A')}
- Hoping For: {self.intake.get('hope', 'N/A')}
- Emotional State: {self.intake.get('emotional_state', 'N/A')}
- Triggers: {self.intake.get('triggers', 'N/A')}
"""
        return context.strip()
    
    def get_characters_context(self):
        """Get tracked characters for agent context"""
        if not self.characters.get("characters"):
            return "No key people identified yet."
        
        context = "KEY PEOPLE IN USER'S LIFE:\n"
        for name, data in self.characters["characters"].items():
            context += f"- {name} ({data.get('relationship', 'unknown')}): {', '.join(data.get('themes', []))}\n"
        
        return context.strip()
    
    def update_character(self, name, relationship=None, themes=None, entry_id=None):
        """Track or update a character mentioned in entries"""
        if name not in self.characters["characters"]:
            self.characters["characters"][name] = {
                "relationship": relationship or "unknown",
                "themes": themes or [],
                "entries_mentioned": []
            }
        
        char = self.characters["characters"][name]
        
        # Update relationship if provided
        if relationship and char["relationship"] == "unknown":
            char["relationship"] = relationship
        
        # Add new themes
        if themes:
            for theme in themes:
                if theme not in char["themes"]:
                    char["themes"].append(theme)
        
        # Track entry
        if entry_id and entry_id not in char["entries_mentioned"]:
            char["entries_mentioned"].append(entry_id)
        
        self._save_json(self.characters_file, self.characters)
    
    def log_entry(self, entry_text, entry_id=None):
        """Log a new journal entry"""
        if not entry_id:
            entry_id = len(self.entries["entries"]) + 1
        
        entry_data = {
            "id": entry_id,
            "timestamp": datetime.now().isoformat(),
            "text": entry_text
        }
        
        self.entries["entries"].append(entry_data)
        self._save_json(self.entries_file, self.entries)
        
        return entry_id
    
    def get_full_context_for_agents(self):
        """
        Compile complete user context for agents
        This is passed to every agent before they respond
        """
        context = {
            "intake": self.get_intake_context(),
            "characters": self.get_characters_context(),
            "entry_count": len(self.entries.get("entries", []))
        }
        
        return context


# Quick test
if __name__ == "__main__":
    scribe = SilentScribe()
    
    print("=== SILENT SCRIBE TEST ===\n")
    print("Intake Context:")
    print(scribe.get_intake_context())
    print("\n" + "-"*50 + "\n")
    print("Characters:")
    print(scribe.get_characters_context())