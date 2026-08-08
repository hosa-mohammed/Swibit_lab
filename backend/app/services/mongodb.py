from pymongo import MongoClient
from datetime import datetime
from app.core.config import settings

client = MongoClient(settings.MONGODB_URL)
db = client.swibit
audit_collection = db.audit_logs


def log_audit(action: str, user_id: int, details: dict = None):
    audit_collection.insert_one({
        "action": action,
        "user_id": user_id,
        "details": details or {},
        "timestamp": datetime.utcnow()
    })


def get_audit_logs(user_id: int = None, limit: int = 100):
    query = {"user_id": user_id} if user_id else {}
    return list(audit_collection.find(query, {"_id": 0}).limit(limit).sort("timestamp", -1))