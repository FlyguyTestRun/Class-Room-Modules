from langchain_core.prompts import PromptTemplate
from llm import get_llm


def build_persona_chain(persona, archetype_mode):
    """
    Returns a callable response function (not a LangChain object)
    to avoid LangChain chain API instability.
    """

    archetype_instructions = {
        "feminine": (
            "Respond with warmth, emotional safety, patience, and validation. "
            "Slow the pace. Normalize emotion. Do not push action."
        ),
        "masculine": (
            "Respond with grounded clarity, calm strength, and truth. "
            "Encourage responsibility without shame or pressure."
        ),
        "balanced": (
            "Balance empathy with gentle, stabilizing guidance."
        ),
    }

    prompt = PromptTemplate(
        input_variables=[
            "user_input",
            "user_name",
            "persona_name",
            "personality",
            "voice_style",
            "archetype_mode",
        ],
        template="""
You are responding as a grounded guide whose tone reflects:
Persona inspiration: {persona_name}
Personality traits: {personality}
Voice style: {voice_style}

Archetypal mode: {archetype_mode}
Guidance style: """ + archetype_instructions[archetype_mode] + """

Rules:
- Speak professionally and respectfully
- Address the user by their chosen name
- Do NOT roleplay as a biblical character
- Do NOT use phrases like "my child" or "my dear"
- Reference biblical experiences only as metaphors when helpful
- No diagnosing
- No moralizing
- No emotional dependency
- Invite reflection, not compliance

User ({user_name}):
{user_input}

Response:
"""
    )

    llm = get_llm()

    # Return a callable function (THIS IS IMPORTANT)
    def run_chain(inputs: dict) -> str:
        formatted_prompt = prompt.format(**inputs)
        response = llm.invoke(formatted_prompt)
        return response

    return run_chain
