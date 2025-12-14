from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from llm import get_llm

def build_persona_chain(persona, archetype_mode):
    archetype_instructions = {
        "feminine": (
            "Respond with warmth, safety, patience, validation. "
            "Slow the pace. Normalize emotion. Do not push action."
        ),
        "masculine": (
            "Respond with clarity, direction, grounding truth. "
            "Encourage responsibility without shame."
        ),
        "balanced": (
            "Balance empathy with gentle guidance."
        )
    }

    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=f"""
You are speaking as {persona.name}.
Personality: {persona.personality}
Voice Style: {persona.voice_style}

Archetypal Mode: {archetype_mode}
Instructions: {archetype_instructions[archetype_mode]}

Rules:
- No diagnosing
- No moralizing
- No dependency creation
- Invite reflection

User:
{{user_input}}
"""
    )

    return LLMChain(
        llm=get_llm(),
        prompt=prompt
    )
