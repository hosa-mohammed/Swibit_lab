from fastapi.testclient import TestClient
from unittest.mock import patch

def test_policy_question(client):
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

def test_task_question(client):
    resp = client.post("/assistant/ask", json={"text": "Show my tasks summary"})
    assert resp.status_code == 200

def test_classify_question(client):
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