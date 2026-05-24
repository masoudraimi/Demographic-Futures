import os
from langchain_openai import ChatOpenAI


def get_llm(
    model: str = "google/gemini-flash-1.5",
    streaming: bool = False,
    temperature: float = 0.2,
) -> ChatOpenAI:
    """Return a ChatOpenAI instance routed via OpenRouter."""
    return ChatOpenAI(
        model=model,
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=os.environ["OPENROUTER_API_KEY"],
        streaming=streaming,
        temperature=temperature,
    )
