import re

try:
    from .biblical_persona import BIBLICAL_VOICES
except Exception:
    from biblical_persona import BIBLICAL_VOICES


def route_persona(user_text: str) -> dict:
    """
    Determines which biblical persona should respond
    based on trigger keyword matching.
    Defaults to John (love/identity) if no strong match.
    """

    text = user_text.lower()
    best_match = None
    highest_score = 0

    for key, persona in BIBLICAL_VOICES.items():
        triggers = persona.get("triggers", [])
        score = 0
        for trigger in triggers:
            trig = (trigger or "").strip().lower()
            if not trig:
                continue
            # match whole words/phrases using word boundaries to avoid partial matches
            if re.search(r"\b" + re.escape(trig) + r"\b", text):
                score += 1

        if score > highest_score:
            highest_score = score
            best_match = persona

    # Fallback: John (secure attachment / love)
    if best_match is None:
        # prefer explicit 'john' persona, otherwise fall back to first available persona
        best_match = BIBLICAL_VOICES.get("john")
        if best_match is None:
            try:
                best_match = next(iter(BIBLICAL_VOICES.values()))
            except StopIteration:
                # no personas defined
                return {}

    return best_match
