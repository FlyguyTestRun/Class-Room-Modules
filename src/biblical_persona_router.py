import re
from config import DEBUG

try:
    from .biblical_persona import BIBLICAL_VOICES
except Exception:
    from biblical_persona import BIBLICAL_VOICES


def route_persona(user_text: str):
    """
    Routes user input to the best-matching biblical persona.
    Returns:
        persona (dict)
        debug_info (dict)
    """

    text = user_text.lower()
    scores = {}
    trigger_hits = {}

    for key, persona in BIBLICAL_VOICES.items():
        score = 0
        hits = []

        for trigger in persona.get("triggers", []):
            trig = (trigger or "").strip().lower()
            if not trig:
                continue
            if re.search(r"\b" + re.escape(trig) + r"\b", text):
                score += 1
                hits.append(trig)

        scores[key] = score
        trigger_hits[key] = hits

    # Determine best match
    best_key = max(scores, key=lambda k: scores[k])
    best_score = scores[best_key]

    # Fallback logic
    if best_score == 0:
        best_key = "john" if "john" in BIBLICAL_VOICES else next(iter(BIBLICAL_VOICES))

    persona = BIBLICAL_VOICES[best_key]

    debug_info = {
        "selected_persona": best_key,
        "scores": scores,
        "trigger_hits": trigger_hits,
        "confidence": compute_confidence(scores)
    }

    return persona, debug_info


def compute_confidence(scores: dict) -> dict:
    """
    Normalizes persona scores into confidence percentages.
    """
    total = sum(scores.values())
    if total == 0:
        return {k: 0.0 for k in scores}

    return {
        k: round(v / total, 3)
        for k, v in scores.items()
    }
