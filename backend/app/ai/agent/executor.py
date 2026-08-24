import logging
from app.ai.agent.tools import search_policies, get_task_summary
from app.ai.classifier import classify_message

logger = logging.getLogger(__name__)


def execute_tool(tool_name: str, query: str, user_id: int = None) -> dict:
    """Run the selected tool."""
    logger.info(f"Executing tool: {tool_name}")
    
    if tool_name == "search_policies":
        return search_policies(query)
    
    elif tool_name == "get_task_summary":
        return get_task_summary(user_id or 1)
    
    elif tool_name == "classify_message":
        return classify_message(query)
    
    else:
        return {"error": f"Unknown tool: {tool_name}"}