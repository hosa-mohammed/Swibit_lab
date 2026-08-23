import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")

client = None
if LLM_API_KEY:
    client = OpenAI(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
    )


def call_llm(system_prompt: str, user_text: str, model: str = "gpt-4o-mini") -> str:
    if client is None:
        raise RuntimeError("LLM client not initialized. Check LLM_API_KEY.")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        timeout=30,
    )
    return response.choices[0].message.content