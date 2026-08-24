from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_policy_question():
    """Scenario 1: User asks about policy."""
    mock_response = {
        "answer": "Employees earn 15 days PTO per year.",
        "citations": ["vacation-policy.md"]
    }
    
    with patch("app.ai.agent.tools.answer_question") as mock:
        mock.return_value = mock_response
        
        resp = client.post("/assistant/ask", json={"text": "How many vacation days?"})
        
        assert resp.status_code == 200
        data = resp.json()
        assert "15 days" in data["answer"]


def test_task_question():
    """Scenario 2: User asks about tasks."""
    resp = client.post("/assistant/ask", json={"text": "Show my tasks summary"})
    
    assert resp.status_code == 200


def test_classify_question():
    """Scenario 3: User reports a bug."""
    mock_response = {
        "category": "support",
        "priority": "high",
        "summary": "App crash",
        "suggested_action": "Investigate"
    }
    
    with patch("app.ai.agent.executor.classify_message") as mock:
        mock.return_value = mock_response
        
        resp = client.post("/assistant/ask", json={"text": "The app crashes!"})
        
        assert resp.status_code == 200