from pathlib import Path
from fastapi import APIRouter, HTTPException

from app.ai.client import call_llm
from app.ai.schemas import MessageIn, ClassificationOut

router = APIRouter(prefix="/assistant", tags=["assistant"])


def load_prompt(filename: str) -> str:
    prompt_path = Path(__file__).parent / "prompts" / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


@router.post("/classify", response_model=ClassificationOut)
async def classify(body: MessageIn):
    try:
        prompt = load_prompt("classifier.md")
        raw = call_llm(prompt, body.text)
        return ClassificationOut.model_validate_json(raw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")