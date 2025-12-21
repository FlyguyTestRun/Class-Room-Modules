DEBUG = True
LOG_FILE_PATH = "healing_vault.log"

"""
Central Configuration for Healing Vault
All system-wide settings in one place
"""

import os
from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SILENT_SCRIBE_DIR = DATA_DIR / "silent_scribe"
SINGLE_BOOKS_DIR = DATA_DIR / "single_books"

# Ensure directories exist
SILENT_SCRIBE_DIR.mkdir(parents=True, exist_ok=True)
SINGLE_BOOKS_DIR.mkdir(parents=True, exist_ok=True)

# Model configuration
EMBEDDING_MODEL = "llama3.1:8b"
LLM_MODEL = "llama3.1:8b"

# Database collections
INTAKE_COLLECTION = "user_intake"
JOURNAL_COLLECTION = "journal_entries"

# Book collections by topic
TRAUMA_BOOKS = {
    "van_der_kolk": "trauma/the_body_keeps_the_score_pdf",
    "levine": "trauma/waking_the_tiger_peter_levine",
    "mate": "trauma/the_myth_of_normal_by_gabor_mate"
}

ATTACHMENT_BOOKS = {
    # Add attachment books here when ready
}

SHADOW_BOOKS = {
    # Add shadow books here when ready
}

# Specialist configurations
SPECIALISTS = {
    "trauma": {
        "name": "Trauma & Nervous System Specialist",
        "icon": "🛡️",
        "books": TRAUMA_BOOKS,
        "trigger_keywords": [
            "flashback", "triggered", "freeze", "panic", "body", "numb",
            "dissociate", "trauma", "ptsd", "nervous system", "somatic",
            "breath", "tension", "rage", "hypervigilant"
        ]
    },
    # Add more specialists as you build them
}

# System settings
MAX_INTAKE_CHUNKS = 6
RESPONSE_TEMPERATURE = 0.7
MAX_SEARCH_RESULTS = 2  # Per book