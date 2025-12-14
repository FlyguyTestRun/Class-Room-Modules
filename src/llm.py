from langchain_community.llms import Ollama

def get_llm():
    return Ollama(
        model="llama3.1:8b",
        temperature=0.6,
        top_p=0.9
    )
