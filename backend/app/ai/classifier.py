import json
import os
from pathlib import Path
from openai import OpenAI

from app.ai.schemas import ClassificationResult

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_prompt(filename: str) -> str:
    prompt_path = Path(__file__).parent / "prompts" / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def classify_message(message: str) -> ClassificationResult:
    system_prompt = load_prompt("classifier.md")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        
        raw_json = response.choices[0].message.content
        data = json.loads(raw_json)
        
        # Pydantic validation
        return ClassificationResult(**data)
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM: {e}")
    except Exception as e:
        raise RuntimeError(f"Classification failed: {e}")