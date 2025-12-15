DEBUG = True  # Set to False in production

from safety_layer import safety_check, safety_response
from biblical_persona_router import route_persona
from archetype_router import archetype_mode
from persona_chain import build_persona_chain


def respond(user_text: str, user_name: str = "User") -> str:
    if DEBUG:
        print(f"\n[DEBUG] Incoming message: {user_text}")
        print(f"[DEBUG] User name: {user_name}")

    # Safety layer
    if safety_check(user_text):
        return safety_response()

    # Persona routing
    persona, persona_debug = route_persona(user_text)

    # Archetype routing (UNPACK CORRECTLY)
    archetype, archetype_debug = archetype_mode(user_text)

    if DEBUG:
        print("\n--- DEBUG LOG ---")
        print("Persona selected:", persona.get("name"))
        print("Trigger matches:", persona_debug.get("trigger_hits"))
        print("Persona scores:", persona_debug.get("scores"))
        print("Confidence blend:", persona_debug.get("confidence"))
        print("Archetype selected:", archetype)
        print("Archetype reason:", archetype_debug.get("reason"))
        print("-----------------\n")

    # Build LLM chain
    chain = build_persona_chain(
        persona=persona,
        archetype_mode=archetype  # <-- STRING ONLY
    )

    # Execute chain
    result = chain({
        "user_input": user_text,
        "user_name": user_name,
        "persona_name": persona["name"],
        "personality": persona["personality"],
        "voice_style": persona["voice_style"],
        "archetype_mode": archetype,
    })

    return result
