import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

with patch.dict(os.environ, {"LLM_API_KEY": "test-key"}):
    with patch("app.ai.rag.retrieve.client") as mock_client:
        mock_client.embeddings.create.return_value = MagicMock(
            data=[MagicMock(embedding=[0.1] * 1536)]
        )
        from app.main import app

client = TestClient(app)

def test_policy_question():
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
    resp = client.post("/assistant/ask", json={"text": "Show my tasks summary"})
    assert resp.status_code == 200

def test_classify_question():
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