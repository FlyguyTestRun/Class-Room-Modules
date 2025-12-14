FEMININE_STATES = [
    "grief", "loss", "shame", "overwhelmed",
    "exhausted", "afraid", "lonely", "abandoned"
]

MASCULINE_STATES = [
    "stuck", "lazy", "avoidant", "directionless",
    "numb", "unmotivated", "adrift"
]

def archetype_mode(text: str) -> str:
    t = text.lower()

    if any(word in t for word in FEMININE_STATES):
        return "feminine"

    if any(word in t for word in MASCULINE_STATES):
        return "masculine"

    return "balanced"

