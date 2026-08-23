import json
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_remote_work():
    mock_chunks = [
        {
            "id": "remote-work-policy.md_0",
            "text": "All full-time employees with 6+ months tenure are eligible for remote work.",
            "source": "remote-work-policy.md",
            "heading": "Eligibility",
            "score": 0.85
        }
    ]
    
    mock_llm = {
        "answer": "All full-time employees with 6+ months tenure are eligible.",
        "citations": ["remote-work-policy.md"]
    }
    
    with patch("app.ai.rag.answer.retrieve") as mock_retrieve:
        mock_retrieve.return_value = mock_chunks
        
        with patch("app.ai.rag.answer.client.chat.completions.create") as mock_create:
            mock_create.return_value.choices[0].message.content = json.dumps(mock_llm)
            
            resp = client.post("/assistant/ask", json={"text": "Who is eligible for remote work?"})
            
            assert resp.status_code == 200
            data = resp.json()
            assert "eligible" in data["answer"].lower()
            assert "remote-work-policy.md" in data["citations"]


def test_vacation():
    mock_chunks = [
        {
            "id": "vacation-policy.md_0",
            "text": "Employees earn 15 days PTO per year.",
            "source": "vacation-policy.md",
            "heading": "Accrual",
            "score": 0.88
        }
    ]
    
    mock_llm = {
        "answer": "Employees earn 15 days PTO per year.",
        "citations": ["vacation-policy.md"]
    }
    
    with patch("app.ai.rag.answer.retrieve") as mock_retrieve:
        mock_retrieve.return_value = mock_chunks
        
        with patch("app.ai.rag.answer.client.chat.completions.create") as mock_create:
            mock_create.return_value.choices[0].message.content = json.dumps(mock_llm)
            
            resp = client.post("/assistant/ask", json={"text": "How many vacation days?"})
            
            assert resp.status_code == 200
            data = resp.json()
            assert "15 days" in data["answer"]


def test_expense():
    mock_chunks = [
        {
            "id": "expense-policy.md_0",
            "text": "Meals: $75/day. Lodging: $200/night.",
            "source": "expense-policy.md",
            "heading": "Limits",
            "score": 0.82
        }
    ]
    
    mock_llm = {
        "answer": "Meals are limited to $75 per day.",
        "citations": ["expense-policy.md"]
    }
    
    with patch("app.ai.rag.answer.retrieve") as mock_retrieve:
        mock_retrieve.return_value = mock_chunks
        
        with patch("app.ai.rag.answer.client.chat.completions.create") as mock_create:
            mock_create.return_value.choices[0].message.content = json.dumps(mock_llm)
            
            resp = client.post("/assistant/ask", json={"text": "What is the meal limit?"})
            
            assert resp.status_code == 200
            data = resp.json()
            assert "$75" in data["answer"]


def test_dont_know_stock():
    with patch("app.ai.rag.answer.retrieve") as mock_retrieve:
        mock_retrieve.return_value = []
        
        resp = client.post("/assistant/ask", json={"text": "What is the stock price?"})
        
        assert resp.status_code == 200
        data = resp.json()
        assert "don't know" in data["answer"].lower()


def test_dont_know_salary():
    with patch("app.ai.rag.answer.retrieve") as mock_retrieve:
        mock_retrieve.return_value = []
        
        resp = client.post("/assistant/ask", json={"text": "What is my salary?"})
        
        assert resp.status_code == 200
        data = resp.json()
        assert "don't know" in data["answer"].lower()


def test_dont_know_health():
    with patch("app.ai.rag.answer.retrieve") as mock_retrieve:
        mock_retrieve.return_value = []
        
        resp = client.post("/assistant/ask", json={"text": "Health insurance?"})
        
        assert resp.status_code == 200
        data = resp.json()
        assert "don't know" in data["answer"].lower()