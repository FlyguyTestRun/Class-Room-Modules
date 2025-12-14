from safety_layer import safety_check, safety_response
from biblical_persona_router import route_persona
from archetype_router import archetype_mode
from persona_chain import build_persona_chain


def respond(user_text: str) -> str:
    """
    Core response engine for the Healing Vault.
    Routes safety → persona → archetype → LLM response.
    """
    if safety_check(user_text):
        return safety_response()

    persona = route_persona(user_text)
    mode = archetype_mode(user_text)

    chain = build_persona_chain(persona, mode)
    return chain.run(user_input=user_text)
