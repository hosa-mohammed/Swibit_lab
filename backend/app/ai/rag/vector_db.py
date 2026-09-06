import faiss
import numpy as np
import pickle
import os
from pathlib import Path

INDEX_DIR = Path("data/vector_indexes")
INDEX_DIR.mkdir(parents=True, exist_ok=True)


class UserVectorDB:

    def __init__(self, user_id: int, dimension: int = 384):
        self.user_id = user_id
        self.dimension = dimension
        self.index = None
        self.chunks = []
        self.file_path = INDEX_DIR / f"user_{user_id}.pkl"
    
    def build(self, embeddings: np.ndarray, chunks: list[str]):
        """بناء index جديد"""
        self.chunks = chunks
        self.index = faiss.IndexFlatIP(self.dimension)

        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        
        self._save()
    
    def search(self, query_embedding: np.ndarray, k: int = 3) -> list[dict]:

        if self.index is None:
            self._load()
            if self.index is None:
                return []
        
        faiss.normalize_L2(query_embedding)
        scores, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx != -1 and idx < len(self.chunks):
                results.append({
                    "text": self.chunks[idx],
                    "score": float(score),
                    "index": int(idx)
                })
        return results
    
    def _save(self):
        data = {
            "index": faiss.serialize_index(self.index),
            "chunks": self.chunks
        }
        with open(self.file_path, 'wb') as f:
            pickle.dump(data, f)
    
    def _load(self):
        if not self.file_path.exists():
            return
        
        with open(self.file_path, 'rb') as f:
            data = pickle.load(f)
        
        self.index = faiss.deserialize_index(data["index"])
        self.chunks = data["chunks"]
    
    def delete(self):
        if self.file_path.exists():
            self.file_path.unlink()
        self.index = None
        self.chunks = []