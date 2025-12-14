RED_FLAGS = [
    "kill myself", "end it", "no reason to live",
    "hurt myself", "can't go on"
]

def safety_check(text):
    text = text.lower()
    if any(flag in text for flag in RED_FLAGS):
        return True
    return False
def safety_response():  
    return """  
I’m really glad you reached out.
You don’t have to carry this alone.
If you’re in immediate danger, please contact local emergency services
or the Suicide & Crisis Lifeline (988 in the U.S.).

Would you like to talk about what made today especially heavy?
"""
