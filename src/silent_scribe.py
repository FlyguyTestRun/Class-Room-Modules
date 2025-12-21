"""
Silent Scribe - Memory & Context Manager
Professional memory system with error handling and logging
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import chromadb
from langchain_community.embeddings import OllamaEmbeddings

from config import (
    SILENT_SCRIBE_DIR,
    EMBEDDING_MODEL,
    INTAKE_COLLECTION,
    JOURNAL_COLLECTION
)


class SilentScribe:
    """
    The memory keeper - tracks everything, speaks to no one
    
    Responsibilities:
    - Store and retrieve intake data
    - Track characters/relationships
    - Log journal entries
    - Provide context to specialists
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize Silent Scribe memory system
        
        Args:
            verbose: If True, print status messages
        """
        self.verbose = verbose
        self._log("Initializing Silent Scribe...")
        
        # File paths
        self.intake_file = SILENT_SCRIBE_DIR / "intake.json"
        self.characters_file = SILENT_SCRIBE_DIR / "characters.json"
        self.entries_file = SILENT_SCRIBE_DIR / "journal_entries.json"
        
        # Load existing data
        self.intake = self._load_json(self.intake_file)
        self.characters = self._load_json(
            self.characters_file,
            default={"characters": {}}
        )
        self.entries = self._load_json(
            self.entries_file,
            default={"entries": []}
        )
        
        # Setup ChromaDB
        try:
            self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
            self.chroma_client = chromadb.PersistentClient(
                path=str(SILENT_SCRIBE_DIR)
            )
            self._log("✓ ChromaDB initialized")
        except Exception as e:
            self._log(f"⚠️  ChromaDB initialization failed: {e}")
            self.chroma_client = None
    
    def _log(self, message: str):
        """Internal logging"""
        if self.verbose:
            print(message)
    
    def _load_json(
        self,
        filepath: Path,
        default: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Safely load JSON file
        
        Args:
            filepath: Path to JSON file
            default: Default value if file doesn't exist
            
        Returns:
            Loaded data or default value
        """
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                self._log(f"⚠️  Error loading {filepath.name}: {e}")
                return default
        return default
    
    def _save_json(self, filepath: Path, data: Dict):
        """
        Safely save JSON file
        
        Args:
            filepath: Path to save to
            data: Data to save
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self._log(f"⚠️  Error saving {filepath.name}: {e}")
    
    def has_intake(self) -> bool:
        """Check if user has completed intake"""
        return self.intake is not None and "story" in self.intake
    
    def get_intake_context(self) -> str:
        """
        Get user's initial intake story for agent context
        
        Returns:
            Formatted intake context or message if not available
        """
        if not self.has_intake():
            return "No intake information available."
        
        name = self.intake.get('name', 'User')
        
        context = f"""
USER BACKGROUND (from intake - {name}):
- Story: {self.intake.get('story', 'N/A')}
- Current Struggle: {self.intake.get('current_struggle', 'N/A')}
- Hoping For: {self.intake.get('hope', 'N/A')}
- Emotional State: {self.intake.get('emotional_state', 'N/A')}
- Known Triggers: {self.intake.get('triggers', 'N/A')}
"""
        return context.strip()
    
    def get_characters_context(self) -> str:
        """
        Get tracked characters for agent context
        
        Returns:
            Formatted character context
        """
        if not self.characters.get("characters"):
            return "No key people identified yet."
        
        context = "KEY PEOPLE IN USER'S LIFE:\n"
        for name, data in self.characters["characters"].items():
            relationship = data.get('relationship', 'unknown')
            themes = ', '.join(data.get('themes', []))
            context += f"- {name} ({relationship}): {themes}\n"
        
        return context.strip()
    
    def get_user_name(self) -> str:
        """Get user's preferred name or default"""
        if self.has_intake():
            return self.intake.get('name', 'friend')
        return 'friend'
    
    def update_character(
        self,
        name: str,
        relationship: Optional[str] = None,
        themes: Optional[List[str]] = None,
        entry_id: Optional[int] = None
    ):
        """
        Track or update a character mentioned in entries
        
        Args:
            name: Person's name or relationship
            relationship: Their relationship to user
            themes: Associated themes/patterns
            entry_id: Journal entry where mentioned
        """
        if name not in self.characters["characters"]:
            self.characters["characters"][name] = {
                "relationship": relationship or "unknown",
                "themes": themes or [],
                "entries_mentioned": []
            }
        
        char = self.characters["characters"][name]
        
        # Update relationship if provided and currently unknown
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
    
    def log_entry(self, entry_text: str, entry_id: Optional[int] = None) -> int:
        """
        Log a new journal entry
        
        Args:
            entry_text: The journal entry content
            entry_id: Optional specific ID
            
        Returns:
            The entry ID assigned
        """
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
    
    def get_full_context_for_agents(self) -> Dict:
        """
        Compile complete user context for agents
        This is passed to every agent before they respond
        
        Returns:
            Dictionary with all user context
        """
        return {
            "user_name": self.get_user_name(),
            "intake": self.get_intake_context(),
            "characters": self.get_characters_context(),
            "entry_count": len(self.entries.get("entries", [])),
            "has_intake": self.has_intake()
        }


# Singleton instance for easy import
_scribe_instance = None

def get_scribe(verbose: bool = False) -> SilentScribe:
    """
    Get or create Silent Scribe singleton
    
    Args:
        verbose: Enable logging
        
    Returns:
        SilentScribe instance
    """
    global _scribe_instance
    if _scribe_instance is None:
        _scribe_instance = SilentScribe(verbose=verbose)
    return _scribe_instance