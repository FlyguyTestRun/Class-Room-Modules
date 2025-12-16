# ---------------------------------------
# HEALING VAULT ENGINE — FINAL STABLE
# ---------------------------------------
"""
Central orchestration engine.

Responsibilities:
- Safety gating
- Persona routing
- Archetype modulation
- Council mode execution
- Single voice fallback
"""

from typing import Dict

from safety_layer import safety_check, safety_response
from biblical_persona_router import route_persona
from archetype_router import archetype_mode
from persona_chain import build_persona_chain

# Optional Council + Memory (fail-safe imports)
try:
    from council_engine import run_council
except ImportError:
    run_council = None

try:
    from memory_scribe import write_scribe_entry
except ImportError:
    def write_scribe_entry(*args, **kwargs):
        pass


# ---------------------------------------
# CONFIGURATION
# ---------------------------------------

DEBUG = True
COUNCIL_CONFIDENCE_THRESHOLD = 0.35


# ---------------------------------------
# MAIN RESPONSE FUNCTION
# ---------------------------------------

def respond(
    user_text: str,
    user_name: str = "User"
) -> str:
    """
    Primary response entry point.
    """

    # -----------------------------
    # SAFETY LAYER
    # -----------------------------
    if safety_check(user_text):
        return safety_response()

    # -----------------------------
    # ARCHETYPE & PERSONA ROUTING
    # -----------------------------
    archetype, archetype_debug = archetype_mode(user_text)
    persona, persona_debug = route_persona(user_text)

    # -----------------------------
    # DEBUG LOGGING
    # -----------------------------
    if DEBUG:
        print("\n--- DEBUG LOG ---")
        print("User:", user_name)
        print("Archetype:", archetype)
        print("Persona selected:", persona.get("name"))
        print("Persona scores:", persona_debug.get("scores"))
        print("Confidence blend:", persona_debug.get("confidence"))
        print("-----------------\n")

    # -----------------------------
    # COUNCIL MODE DECISION
    # -----------------------------
    persona_confidence: Dict = persona_debug.get("confidence", {})

    eligible_for_council = (
        run_council is not None
        and sum(1 for c in persona_confidence.values() if c >= COUNCIL_CONFIDENCE_THRESHOLD) > 1
    )

    if eligible_for_council:
        return run_council(
            user_text=user_text,
            user_name=user_name,
            persona_confidence=persona_debug,
            archetype=archetype
        )

    # -----------------------------
    # SINGLE PERSONA FALLBACK
    # -----------------------------
    chain = build_persona_chain(
        persona=persona,
        archetype_mode=archetype
    )

    output = chain.invoke({
        "user_input": user_text,
        "user_name": user_name,
        "persona_name": persona["name"],
        "personality": persona["personality"],
        "voice_style": persona["voice_style"],
        "archetype_mode": archetype,
        "archetype_instruction": archetype
    })

    # -----------------------------
    # MEMORY SCRIBE (SILENT)
    # -----------------------------
    write_scribe_entry(
        user_text=user_text,
        reflections=[output]
    )

    return output
