from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.classifier import classify_message
from app.ai.extractor import extract_info
from app.ai.schemas import ClassificationResult, ExtractionResult

router = APIRouter(prefix="/ai", tags=["ai"])


class MessageRequest(BaseModel):
    message: str


@router.post("/classify", response_model=ClassificationResult)
async def classify_endpoint(request: MessageRequest):
    try:
        result = classify_message(request.message)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract", response_model=ExtractionResult)
async def extract_endpoint(request: MessageRequest):
    try:
        result = extract_info(request.message)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))