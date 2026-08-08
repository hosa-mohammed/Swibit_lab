from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.logging import logger
from app.api.deps import get_current_user
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.cache import get_cached_tasks, set_cached_tasks
from app.services.mongodb import log_audit  # ← جديد

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info("Listing tasks", extra={"user_id": current_user.id})
    
    cached = get_cached_tasks(current_user.id)
    if cached:
        logger.info("Cache hit", extra={"user_id": current_user.id})
        return cached
    
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    set_cached_tasks(current_user.id, tasks)
    logger.info("Cache miss - fetched from DB", extra={"user_id": current_user.id})
    return tasks


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info("Creating task", extra={"user_id": current_user.id, "title": task.title})
    
    db_task = Task(**task.dict(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    

    log_audit("task_created", current_user.id, {"task_id": db_task.id, "title": task.title})
    
    logger.info("Task created", extra={"task_id": db_task.id})
    return db_task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    
    log_audit("task_updated", current_user.id, {"task_id": task_id})
    return db_task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    
    log_audit("task_deleted", current_user.id, {"task_id": task_id})
    return {"message": "Task deleted"}