import json
import os
from pathlib import Path
from openai import OpenAI

from app.ai.schemas import ExtractionResult

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_prompt(filename: str) -> str:
    prompt_path = Path(__file__).parent / "prompts" / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_info(message: str) -> ExtractionResult:
    system_prompt = load_prompt("extractor.md")
    
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
        return ExtractionResult(**data)
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM: {e}")
    except Exception as e:
        raise RuntimeError(f"Extraction failed: {e}")