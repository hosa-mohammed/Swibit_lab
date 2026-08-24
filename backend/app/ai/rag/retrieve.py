import os
import math

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("LLM_API_KEY", "test-key"))
except Exception:
    client = None

class VectorStore:
    def __init__(self):
        self.docs = []
        self.vectors = []
    
    def add(self, documents):
        self.docs = documents
        texts = [d["text"] for d in documents]
        self.vectors = self.embed(texts)
    
    def embed(self, texts):
        if client is None:
            return [[0.0] * 1536 for _ in texts]
        resp = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        return [item.embedding for item in resp.data]
    
    def search(self, query, k=3):
        q_vec = self.embed([query])[0]
        results = []
        for i, vec in enumerate(self.vectors):
            score = cosine_sim(q_vec, vec)
            results.append((score, i))
        results.sort(reverse=True)
        out = []
        for score, i in results[:k]:
            item = self.docs[i].copy()
            item["score"] = score
            out.append(item)
        return out

def cosine_sim(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    return dot / (mag_a * mag_b)

_store = None

def get_store():
    global _store
    if _store is None:
        _store = VectorStore()
        from app.ai.rag.ingest import load_documents
        docs = load_documents()
        _store.add(docs)
    return _store

def retrieve(query, k=3):
    store = get_store()
    return store.search(query, k)