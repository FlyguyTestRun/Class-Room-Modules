FEMININE_STATES = [
    "grief", "loss", "shame", "overwhelmed",
    "exhausted", "afraid", "lonely", "abandoned"
]

MASCULINE_STATES = [
    "stuck", "lazy", "avoidant", "directionless",
    "numb", "unmotivated", "adrift"
]

from config import DEBUG

def archetype_mode(user_text: str):
    text = user_text.lower()

    if any(word in text for word in ["overwhelmed", "tired", "exhausted", "hurt"]):
        mode = "feminine"
    elif any(word in text for word in ["stuck", "confused", "lost", "direction"]):
        mode = "balanced"
    else:
        mode = "masculine"

    debug_info = {
        "archetype": mode,
        "reason": "keyword-based heuristic"
    }

    return mode, debug_info
