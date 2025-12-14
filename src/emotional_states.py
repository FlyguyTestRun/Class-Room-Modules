EMOTIONAL_STATES = {
    "shame": ["ashamed", "disgusted with myself", "unworthy"],
    "grief": ["loss", "miss", "gone", "never again"],
    "fear": ["scared", "afraid", "anxious", "panic"],
    "anger": ["angry", "rage", "furious"],
    "exhaustion": ["tired", "burned out", "overwhelmed"],
    "calling": ["purpose", "calling", "meant to", "why am I here"]
}

def detect_emotional_state(text):
    text = text.lower()
    scores = {k: 0 for k in EMOTIONAL_STATES}
    for state, words in EMOTIONAL_STATES.items():
        for w in words:
            if w in text:
                scores[state] += 1
    return max(scores, key=scores.get)
