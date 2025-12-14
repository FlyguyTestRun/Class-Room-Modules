# Healing Vault - Council of Friends™

An AI-powered mental health companion providing personalized therapeutic support through specialized AI personas.

## 🚧 Development Status
Currently building MVP - Private portfolio project

## Tech Stack
- **Language:** Python 3.13
- **LLM:** Ollama (Llama 3.1)
- **UI:** Streamlit
- **Vector DB:** ChromaDB  
- **RAG Framework:** LangChain

## Features (Planned)
- Multi-persona therapeutic responses
- Book-grounded advice (50+ psychology/therapy texts)
- Pattern recognition across journal entries
- Local-first (all data stored on device)
- Privacy-focused (no cloud uploads)

## Architecture
```
src/          # Core application code
data/         # PDFs and vector embeddings (gitignored)
docs/         # Documentation and architecture notes
tests/        # Unit tests
```

## Author
Bryan Shaw - Building as demonstration of RAG architecture and LLM integration skills, planned implementation to App. 

## Vision: Biblical Personas as Sub-Agents
One generic "Gentle Father" 

New Testament Voices:

Paul - Theologian, grace doctor, former persecutor (Romans, Galatians, Ephesians, etc.)

Peter - Impulsive fisherman turned rock, restoration expert (1 & 2 Peter)

John - Mystic, beloved disciple, love & light (John's Gospel, 1-3 John, Revelation)

James - Practical wisdom, faith + works (James)

Matthew - Tax collector, Kingdom focus (Matthew's Gospel)

Luke - Physician, compassion for outcasts (Luke, Acts)

Old Testament Voices:

David - Psalmist, man after God's heart, brokenness & worship (Psalms)

Solomon - Wisdom, Proverbs, practical counsel

Isaiah - Prophet, suffering servant, Messiah prophecies

Jeremiah - Weeping prophet, lament & hope




## License
Private - All Rights Reserved
```

**What this does:** AI Agent Spiritual Healing Program & Subagent Blueprints
This is a new program to act as a healing assistant for self-awareness, reflection and assistance in spiritual healing from the trauma of life and relationship challenges we endure. Not therapy advise but to provide a summary to aid theraputic insights and assist in delevering these insights in correlation with therapy. This app will have a memory of all entries by the user, record keeping with timestamps and pattern recognition. Using Ollama and Mistral LLMs  the program validating causation to the end user will journal entries to be interpreted and correlated to psychological books and biblical wisdom for reflection and healing purposes. 
	The journal entries will be stored for future recall comparison and collaboration. 
Healing Vault – Council of Friends™ (Summary)
What it is A private, AI-powered “council of friends” that disciple lives on your phone or desktop. You type one journal entry → 3–6 generated responses from AI independant and focused AI personalities who understand that pain speak back in their own distinct voices → one gentle spiritual father always closes with a short prayer. Nothing is ever shared without consent. Everything is remembered.

Architecture: True Multi-Voice Council
How It Works:

User writes journal entry
Trigger system scores each friend 0-100
Friends scoring >70 respond in sequence (3-6 typically)
Each friend speaks in their own distinct voice
The Gentle Father always closes last (if triggered)
Silent Scribe records everything silently

Architecture: True Multi-Voice Council
How It Works:

User writes journal entry
Trigger system scores each friend 0-100
Friends scoring >70 respond in sequence (3-6 typically)
Each friend speaks in their own distinct voice
The Gentle Father always closes last (if triggered)
Silent Scribe records everything silently
