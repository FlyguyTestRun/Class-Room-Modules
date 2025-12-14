from biblical_persona_router import route_persona

cases = [
    ("I feel shame about my past", "paul"),
    ("I feel like an outcast and a sinner", "matthew"),
    ("I need love and belonging", "john"),
    ("I need to do the right thing", "james"),
    ("I was denied and felt like a coward", "peter"),
    ("", "john"),  # fallback
]

for text, expected in cases:
    persona = route_persona(text)
    pid = persona.get("id") if isinstance(persona, dict) else str(persona)
    print(f"INPUT: {text!r} -> SELECTED: {pid} ; expected: {expected}")
