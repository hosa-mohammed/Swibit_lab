import json
import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_cached_tasks(user_id: int):
    key = f"tasks:user:{user_id}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def set_cached_tasks(user_id: int, tasks):
    key = f"tasks:user:{user_id}"

    tasks_data = [{"id": t.id, "title": t.title, "description": t.description, 
                   "priority": t.priority, "is_complete": t.is_complete, "owner_id": t.owner_id} 
                  for t in tasks]
    redis_client.setex(key, 300, json.dumps(tasks_data)) 