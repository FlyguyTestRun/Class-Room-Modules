"""
Initial Intake System - Healing Vault
Quick 7-minute spiritual inventory to begin the healing journey
Inspired by Regeneration's self-awareness model
"""

import streamlit as st
import json
import os
from datetime import datetime
import chromadb
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
import random

# Configuration
EMBEDDING_MODEL = "llama3.1:8b"
LLM_MODEL = "llama3.1:8b"
SILENT_SCRIBE_PATH = "./data/silent_scribe"
INTAKE_COLLECTION = "user_intake"

st.set_page_config(
    page_title="Healing Vault - Begin Your Journey",
    page_icon="🕊️",
    layout="centered"
)

# Initialize Silent Scribe storage
os.makedirs(SILENT_SCRIBE_PATH, exist_ok=True)

# Varied language for personalization
GREETING_VARIANTS = [
    "Welcome. This is a safe space for your healing journey.",
    "You've arrived. This is your sanctuary for transformation.",
    "Thank you for being here. This space honors your courage.",
    "Welcome, friend. You've taken a brave step by showing up today."
]

NAME_PROMPTS = [
    "Before we begin, what should I call you?",
    "I'd like to know - what name feels right for you here?",
    "What would you like to be called in this space?",
    "How should I address you on this journey?"
]

COMPLETION_MESSAGES = [
    "Your story has been received with care and stored safely.",
    "Thank you for trusting me with your story. It's been recorded with reverence.",
    "Your words are now held safely in the Silent Scribe.",
    "I've received your story. It's stored securely and will guide our work together."
]

def save_intake(intake_data):
    """Save intake responses to Silent Scribe memory"""
    
    # Save as JSON for easy retrieval
    intake_file = os.path.join(SILENT_SCRIBE_PATH, "intake.json")
    with open(intake_file, 'w') as f:
        json.dump(intake_data, f, indent=2)
    
    # Also embed into ChromaDB for semantic search
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    chroma_client = chromadb.PersistentClient(path=SILENT_SCRIBE_PATH)
    
    try:
        collection = chroma_client.get_collection(INTAKE_COLLECTION)
        chroma_client.delete_collection(INTAKE_COLLECTION)
    except:
        pass
    
    collection = chroma_client.create_collection(INTAKE_COLLECTION)
    
    # Create searchable document from intake
    intake_text = f"""
    Name: {intake_data.get('name', 'Not provided')}
    User's Story: {intake_data['story']}
    Current Struggle: {intake_data['current_struggle']}
    Hoping For: {intake_data['hope']}
    Emotional State: {intake_data['emotional_state']}
    What Triggers Me: {intake_data['triggers']}
    """
    
    embedding = embeddings.embed_query(intake_text)
    
    collection.add(
        ids=["intake_baseline"],
        embeddings=[embedding],
        documents=[intake_text],
        metadatas=[{
            "timestamp": intake_data['timestamp'],
            "type": "intake",
            "name": intake_data.get('name', 'Anonymous')
        }]
    )
    
    return True

def extract_initial_characters(story_text):
    """
    Use AI to identify key people mentioned in initial story
    Non-intrusive - just captures who they naturally mention
    """
    llm = Ollama(model=LLM_MODEL, temperature=0.3)
    
    prompt = f"""Read this person's story and identify the key people they mention.

Story:
"{story_text}"

For each person mentioned, extract:
1. Name or relationship (e.g., "Dad", "my ex Sarah", "boss")
2. Their role in the story
3. The emotional tone when describing them

Respond ONLY with JSON (no other text):
{{
  "characters": [
    {{"name": "...", "role": "...", "emotional_tone": "..."}}
  ]
}}"""
    
    try:
        response = llm.invoke(prompt)
        # Clean response
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
        
        characters_data = json.loads(response.strip())
        return characters_data.get("characters", [])
    except:
        return []

def detect_name_in_text(text):
    """Check if user naturally mentioned their name in their story"""
    llm = Ollama(model=LLM_MODEL, temperature=0.3)
    
    prompt = f"""Does this person mention their own name in their story?

Text:
"{text}"

Respond ONLY with JSON:
{{
  "name_mentioned": true/false,
  "name": "their name if found, or null"
}}"""
    
    try:
        response = llm.invoke(prompt)
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
        
        data = json.loads(response.strip())
        if data.get("name_mentioned") and data.get("name"):
            return data["name"]
    except:
        pass
    
    return None

# Title
st.markdown("<h1 style='text-align: center;'>🕊️</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Begin Your Healing Journey</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>A 7-minute spiritual inventory</p>", unsafe_allow_html=True)

st.markdown("---")

# Check if already completed
intake_file = os.path.join(SILENT_SCRIBE_PATH, "intake.json")
if os.path.exists(intake_file):
    with open(intake_file, 'r') as f:
        existing_data = json.load(f)
    
    user_name = existing_data.get('name', 'friend')
    
    st.success(f"✓ Welcome back, {user_name}. Your initial intake is complete.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📖 View My Intake", use_container_width=True):
            st.session_state.show_intake = True
    
    with col2:
        if st.button("🔄 Retake Intake", use_container_width=True):
            st.session_state.confirm_retake = True
    
    if st.session_state.get('show_intake'):
        with st.expander("Your Initial Story", expanded=True):
            st.markdown(f"**Name:** {existing_data.get('name', 'Not provided')}")
            st.markdown(f"**What brought you here:** {existing_data['story']}")
            st.markdown(f"**Current struggle:** {existing_data['current_struggle']}")
            st.markdown(f"**Hoping for:** {existing_data['hope']}")
            st.markdown(f"**Emotional state:** {existing_data['emotional_state']}")
            st.markdown(f"**Triggers:** {existing_data['triggers']}")
            st.markdown(f"**Recorded:** {existing_data['timestamp']}")
    
    if st.session_state.get('confirm_retake'):
        st.warning("⚠️ This will erase your previous intake. Are you sure?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, Start Over", type="primary"):
                os.remove(intake_file)
                st.session_state.show_intake = False
                st.session_state.confirm_retake = False
                st.rerun()
        with col2:
            if st.button("Cancel"):
                st.session_state.confirm_retake = False
                st.rerun()
    
    st.stop()

# Introduction with varied greeting
greeting = random.choice(GREETING_VARIANTS)

st.markdown(f"""
{greeting}

**What happens here:**
- You'll answer 5 questions about your story
- Your responses are stored in the Silent Scribe (private, on your device)
- All healing agents will have this context to support you better
- You can revisit and update this anytime

**Inspired by Regeneration:** Like a spiritual 12-step inventory, we can only address what you're aware of. Let your words guide the path to deeper self-awareness.

*Take your time. There are no wrong answers.*
""")

st.markdown("---")

# The 5 Core Questions
st.subheader("📝 Your Story Begins Here")

with st.form("intake_form"):
    
    st.markdown("### 1. What brings you here today?")
    st.caption("In your own words, why are you reaching out right now?")
    story = st.text_area(
        "Your story:",
        height=120,
        placeholder="I'm here because...",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### 2. What's the hardest thing you're facing right now?")
    st.caption("The struggle that feels most heavy today")
    current_struggle = st.text_area(
        "Current struggle:",
        height=100,
        placeholder="Right now, the hardest thing is...",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### 3. What are you hoping to find here?")
    st.caption("What would healing look like for you?")
    hope = st.text_area(
        "Your hope:",
        height=100,
        placeholder="I'm hoping for...",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### 4. How would you describe your emotional state lately?")
    st.caption("One word, a sentence, or a paragraph - whatever feels right")
    emotional_state = st.text_area(
        "Emotional state:",
        height=80,
        placeholder="Lately I've been feeling...",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("### 5. What triggers you most?")
    st.caption("Situations, people, memories - what sends you into reaction?")
    triggers = st.text_area(
        "My triggers:",
        height=100,
        placeholder="I get triggered when...",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    submitted = st.form_submit_button("🕊️ Begin My Healing Journey", use_container_width=True)

# Process form submission (OUTSIDE the form)
if submitted:
    # Validate
    if not story or not current_struggle or not hope:
        st.error("Please answer at least the first three questions to begin.")
    else:
        with st.spinner("Receiving your story..."):
            
            # Check if name was mentioned naturally
            detected_name = detect_name_in_text(story)
            
            # If no name detected, ask for it
            user_name = None
            if not detected_name:
                st.markdown("---")
                name_prompt = random.choice(NAME_PROMPTS)
                st.markdown(f"### {name_prompt}")
                st.caption("This helps me address you personally. You can use your first name, a nickname, or any name that feels right.")
                
                # Use a text input outside the form
                user_name = st.text_input(
                    "Your name:",
                    placeholder="What should I call you?",
                    label_visibility="collapsed",
                    key="name_input"
                )
                
                if not user_name:
                    st.warning("Please enter a name to continue, or type 'Friend' if you prefer to remain anonymous.")
                    st.stop()
            else:
                user_name = detected_name
                st.info(f"✓ I'll call you {user_name}")
            
            # Prepare intake data
            intake_data = {
                "timestamp": datetime.now().isoformat(),
                "name": user_name,
                "story": story,
                "current_struggle": current_struggle,
                "hope": hope,
                "emotional_state": emotional_state if emotional_state else "Not specified",
                "triggers": triggers if triggers else "Not specified"
            }
            
            # Extract characters mentioned
            with st.spinner("Identifying key people in your story..."):
                all_text = f"{story} {current_struggle} {hope}"
                characters = extract_initial_characters(all_text)
                intake_data["initial_characters"] = characters
            
            # Save to Silent Scribe
            save_intake(intake_data)
            
            completion_message = random.choice(COMPLETION_MESSAGES)
            st.success(f"✅ {completion_message}")
            
            # Show what was captured
            st.markdown("---")
            st.subheader("🗂️ Stored in Your Silent Scribe")
            
            with st.expander("Your Initial Intake", expanded=True):
                st.markdown(f"**Name:** {user_name}")
                if len(story) > 200:
                    st.markdown(f"**Story:** {story[:200]}...")
                else:
                    st.markdown(f"**Story:** {story}")
                st.markdown(f"**Current Struggle:** {current_struggle}")
                st.markdown(f"**Hoping For:** {hope}")
            
            if characters:
                st.markdown("**Key People Identified:**")
                for char in characters:
                    st.text(f"• {char.get('name', 'Unknown')} - {char.get('role', '')}")
            
            st.markdown("---")
            st.balloons()
            
            journey_starts = [
                f"✅ **Your journey begins now, {user_name}**",
                f"✅ **Welcome to your healing journey, {user_name}**",
                f"✅ **{user_name}, your path to healing starts here**",
                f"✅ **The work begins with you, {user_name}**"
            ]
            
            st.success(f"""
            {random.choice(journey_starts)}
            
            
            **Next Step:** You can now close this window and begin journaling. Your healing journey awaits.
            """)
            
            st.info("💡 **Tip:** Bookmark this page to update your intake anytime")