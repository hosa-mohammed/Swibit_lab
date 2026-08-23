import json
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_classify_success():
    mock_response = {
        "category": "support",
        "priority": "high",
        "summary": "App crashes during login",
        "suggested_action": "Investigate login crash issue",
    }
    
    with patch("app.ai.client.client") as mock_client:
        mock_client.chat.completions.create.return_value.choices[0].message.content = json.dumps(mock_response)
        
        response = client.post("/assistant/classify", json={"text": "The app crashes when I try to login"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "support"
        assert data["priority"] == "high"
        assert "summary" in data
        assert "suggested_action" in data


def test_classify_invalid_input():
    response = client.post("/assistant/classify", json={"text": ""})
    assert response.status_code == 422


def test_classify_llm_error():
    with patch("app.ai.client.client") as mock_client:
        mock_client.chat.completions.create.side_effect = Exception("LLM API error")
        
        response = client.post("/assistant/classify", json={"text": "Test message"})
        
        assert response.status_code == 500
        assert "Classification failed" in response.json()["detail"]