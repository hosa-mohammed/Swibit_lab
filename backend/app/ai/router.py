from pathlib import Path
from fastapi import APIRouter, HTTPException

from app.ai.client import call_llm
from app.ai.schemas import MessageIn, ClassificationOut
from app.ai.rag.answer import answer_question

router = APIRouter(prefix="/assistant", tags=["assistant"])


def load_prompt(filename):
    path = Path(__file__).parent / "prompts" / filename
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@router.post("/classify", response_model=ClassificationOut)
async def classify(body: MessageIn):
    try:
        prompt = load_prompt("classifier.md")
        raw = call_llm(prompt, body.text)
        return ClassificationOut.model_validate_json(raw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


@router.post("/ask")
async def ask(body: MessageIn):
    try:
        result = answer_question(body.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Answer failed: {str(e)}")