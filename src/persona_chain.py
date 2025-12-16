# ---------------------------------------
# PERSONA CHAIN BUILDER — FINAL STABLE
# ---------------------------------------
"""
Builds a single, isolated persona response chain.

Design principles:
- One voice per chain
- No cross-persona contamination
- Archetype modulation without identity loss
- LangChain Runnable output (invoke-safe)
"""

from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_community.chat_models import ChatOllama


# ---------------------------------------
# MODEL CONFIGURATION
# ---------------------------------------

DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_TEMPERATURE = 0.6


# ---------------------------------------
# SYSTEM PROMPT TEMPLATE
# ---------------------------------------

SYSTEM_PROMPT = """
You are {persona_name}.

You are speaking as a distinct, historically grounded voice with the following traits:

PERSONALITY:
{personality}

VOICE STYLE:
{voice_style}

ARCHETYPE MODE:
{archetype_mode}

ARCHETYPE INSTRUCTION:
{archetype_instruction}

Rules you must follow:
- Speak ONLY from this persona's perspective
- Do NOT reference other personas
- Do NOT explain system mechanics
- Do NOT offer medical or legal advice
- Maintain emotional safety and clarity
- Avoid absolutist or shaming language
"""


# ---------------------------------------
# BUILD PERSONA CHAIN
# ---------------------------------------

def build_persona_chain(
    persona: Dict,
    archetype_mode: str
) -> Runnable:
    """
    Returns a LangChain Runnable configured for a single persona.

    Parameters:
    - persona: dictionary defining the persona identity and voice
    - archetype_mode: modulation layer (e.g. 'healer', 'shepherd', 'witness')

    Returns:
    - Runnable chain with .invoke() support
    """

    # Validate persona structure early (fail fast, fail clean)
    required_keys = ["name", "personality", "voice_style"]
    for key in required_keys:
        if key not in persona:
            raise ValueError(f"Persona missing required key: {key}")

    # Model (local, deterministic)
    llm = ChatOllama(
        model=DEFAULT_MODEL,
        temperature=DEFAULT_TEMPERATURE
    )

    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{user_input}")
    ])

    # Runnable chain
    chain: Runnable = prompt | llm

    return chain
