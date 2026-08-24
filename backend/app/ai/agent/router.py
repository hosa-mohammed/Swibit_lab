import logging
logger = logging.getLogger(__name__)

def route_query(text: str) -> str:
    """Choose tool based on keywords."""
    text_lower = text.lower()
    
    # Policy questions
    policy_words = ["policy", "vacation", "expense", "remote", "work", "leave", "pto"]
    if any(word in text_lower for word in policy_words):
        logger.info(f"Tool selected: search_policies for query: {text[:50]}")
        return "search_policies"
    
    # Task questions
    task_words = ["task", "my tasks", "summary", "todo", "pending"]
    if any(word in text_lower for word in task_words):
        logger.info(f"Tool selected: get_task_summary for query: {text[:50]}")
        return "get_task_summary"
    
    # Default: classify
    logger.info(f"Tool selected: classify_message for query: {text[:50]}")
    return "classify_message"