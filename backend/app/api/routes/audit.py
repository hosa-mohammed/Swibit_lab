from fastapi import APIRouter, Depends
from typing import List
from app.api.deps import get_current_user
from app.models.user import User
from app.services.mongodb import log_audit, get_audit_logs

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/logs")
def list_logs(current_user: User = Depends(get_current_user)):
    return get_audit_logs(user_id=current_user.id)


@router.post("/log")
def create_log(action: str, current_user: User = Depends(get_current_user)):
    log_audit(action, current_user.id, {"source": "manual"})
    return {"message": "Logged"}