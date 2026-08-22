
import json
import os
from pathlib import Path


def mock_llm_classify(message: str) -> dict:
    """Smart mock based on keywords in the message"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["crash", "error", "bug", "login", "broken"]):
        return {
            "category": "support",
            "priority": "high",
            "summary": f"Technical issue: {message[:50]}",
            "suggested_action": "Investigate and fix the issue"
        }
    elif any(word in message_lower for word in ["cost", "price", "plan", "premium", "subscribe"]):
        return {
            "category": "sales",
            "priority": "low",
            "summary": f"Pricing question: {message[:50]}",
            "suggested_action": "Provide pricing information"
        }
    elif any(word in message_lower for word in ["charge", "bill", "invoice", "payment", "refund"]):
        return {
            "category": "billing",
            "priority": "medium",
            "summary": f"Billing issue: {message[:50]}",
            "suggested_action": "Review billing records"
        }
    elif any(word in message_lower for word in ["terrible", "worst", "bad", "complaint"]):
        return {
            "category": "complaint",
            "priority": "high",
            "summary": f"Customer complaint: {message[:50]}",
            "suggested_action": "Address customer concerns immediately"
        }
    else:
        return {
            "category": "general",
            "priority": "low",
            "summary": f"General message: {message[:50]}",
            "suggested_action": "Reply with helpful information"
        }


def mock_llm_extract(message: str) -> dict:
    """Mock information extraction"""
    message_lower = message.lower()
    
    requester_name = None
    if ":" in message:
        possible_name = message.split(":")[0].strip()
        if len(possible_name) < 20 and " " not in possible_name:
            requester_name = possible_name
    
    if any(word in message_lower for word in ["when", "how", "what", "?"]):
        request_type = "question"
    elif any(word in message_lower for word in ["update", "change", "fix", "modify"]):
        request_type = "update"
    else:
        request_type = "new_task"
    
    if any(word in message_lower for word in ["urgent", "asap", "immediately", "critical", "down"]):
        urgency = "high"
    elif any(word in message_lower for word in ["when you have time", "no rush", "later"]):
        urgency = "low"
    else:
        urgency = "medium"
    
    task_title_guess = None
    if request_type in ["new_task", "update"]:
        words = message_lower.replace("?", "").replace("!", "").split()
        if len(words) > 3:
            task_title_guess = " ".join(words[-5:]).title()
    
    return {
        "requester_name": requester_name,
        "request_type": request_type,
        "urgency": urgency,
        "task_title_guess": task_title_guess
    }


if __name__ == "__main__":
    print("=" * 50)
    print("CLASSIFIER TEST")
    print("=" * 50)
    
    test_messages = [
        "The app crashes when I try to login",
        "How much does the premium plan cost?",
        "I was charged twice for last month",
        "Your service is terrible, I want a refund",
        "Thank you for your help today",
    ]
    
    for msg in test_messages:
        result = mock_llm_classify(msg)
        print(f"\nMessage: {msg}")
        print(f"Category: {result['category']}")
        print(f"Priority: {result['priority']}")
        print(f"Summary: {result['summary']}")
        print(f"Action: {result['suggested_action']}")
    
    print("\n" + "=" * 50)
    print("EXTRACTOR TEST")
    print("=" * 50)
    
    test_extracts = [
        "Ahmed: I need to add a new dashboard page",
        "When will the website update be finished?",
        "URGENT: The website is down! Need fix now",
        "Please update the deadline for task 123",
        "How do I create a recurring task?",
    ]
    
    for msg in test_extracts:
        result = mock_llm_extract(msg)
        print(f"\nMessage: {msg}")
        print(f"Requester: {result['requester_name']}")
        print(f"Type: {result['request_type']}")
        print(f"Urgency: {result['urgency']}")
        print(f"Title: {result['task_title_guess']}")