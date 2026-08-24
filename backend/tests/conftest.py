import os

os.environ["LLM_API_KEY"] = "test-key"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["MONGODB_URL"] = "mongodb://localhost:27017/swibit"

from unittest.mock import MagicMock
import sys

mock_client = MagicMock()
mock_client.embeddings.create.return_value = MagicMock(
    data=[MagicMock(embedding=[0.1] * 1536)]
)
mock_client.chat.completions.create.return_value = MagicMock(
    choices=[MagicMock(message=MagicMock(content='{"answer": "test", "citations": []}'))]
)

sys.modules['openai'] = MagicMock()
sys.modules['openai'].OpenAI = MagicMock(return_value=mock_client)

# Mock Redis و MongoDB
sys.modules['redis'] = MagicMock()
sys.modules['motor'] = MagicMock()
sys.modules['motor.motor_asyncio'] = MagicMock()

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()