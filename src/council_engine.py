# ---------------------------------------
# COUNCIL MODE — MULTI-VOICE ORCHESTRATION
# ---------------------------------------

from persona_chain import build_persona_chain

try:
    from memory_scribe import write_scribe_entry
except ImportError:
    def write_scribe_entry(*args, **kwargs):
        pass  # Safe fallback

MAX_VOICES = 2  # trauma-safe limit


def run_council(
    user_text: str,
    user_name: str,
    persona_confidence: dict,
    archetype: str
) -> str:
    """
    Executes a confidence-weighted, multi-voice council response.
    """

    # Sort personas by confidence score
    sorted_personas = sorted(
        persona_confidence.items(),
        key=lambda item: item[1]["score"],
        reverse=True
    )

    responses = []
    voices_used = 0

    for persona_key, payload in sorted_personas:
        if payload["score"] <= 0 or voices_used >= MAX_VOICES:
            break

        persona = payload["persona"]

        chain = build_persona_chain(
            persona=persona,
            archetype_mode=archetype
        )

        result = chain.invoke({
            "user_input": user_text,
            "user_name": user_name,
            "persona_name": persona["name"],
            "personality": persona["personality"],
            "voice_style": persona["voice_style"],
            "archetype_mode": archetype
        })

        responses.append(result)
        voices_used += 1

    # Silent Scribe (non-decaying memory)
    write_scribe_entry(
        user_text=user_text,
        reflections=responses
    )

    return "\n\n".join(responses)
