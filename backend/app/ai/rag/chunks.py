from sqlalchemy.orm import Session
from app.models.task import Task

def get_user_tasks_text(db: Session, user_id: int) -> str:
    tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    
    lines = []
    for t in tasks:
        if t.completed:
            status = "مكتملة"
        else:
            status = "قيد التنفيذ"
        priority = getattr(t, 'priority', 'medium')
        due = getattr(t, 'due_date', 'غير محدد')
        
        line = (
            f"مهمة #{t.id}: {t.title}\n"
            f"الوصف: {t.description or 'لا يوجد وصف'}\n"
            f"الحالة: {status} | الأولوية: {priority} | الموعد: {due}\n"

            )
        lines.append(line)
    
    return "\n".join(lines)


def chunk_tasks(text: str, chunk_size: 300, overlap: 50) -> list[str]:
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    
    return chunks


def build_user_chunks(db: Session, user_id: int) -> list[str]:
    text = get_user_tasks_text(db, user_id)
    if not text.strip():
        return []
    return chunk_tasks(text)