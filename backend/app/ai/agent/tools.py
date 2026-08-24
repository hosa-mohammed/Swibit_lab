from app.ai.rag.answer import answer_question

def search_policies(query: str) -> dict:
    """Search company policy documents."""
    return answer_question(query)


def get_task_summary(user_id: int) -> dict:
    """Get summary of user tasks."""
    return {
        "total": 5,
        "completed": 3,
        "pending": 2,
        "message": f"User {user_id} has 5 tasks: 3 done, 2 pending"
    }