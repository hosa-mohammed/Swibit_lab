import json
from pathlib import Path
from app.ai.client import call_llm


def load_prompt(filename: str) -> str:
    prompt_path = Path(__file__).parent / "prompts" / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def classify_message(message: str) -> dict:
    """Classify a message using the classifier prompt."""
    system_prompt = load_prompt("classifier.md")
    raw = call_llm(system_prompt, message)
    return json.loads(raw)