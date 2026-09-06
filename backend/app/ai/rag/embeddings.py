import numpy as np
from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def embed_chunks(chunks: list[str]) -> np.ndarray:
    model = get_model()
    embeddings = model.encode(chunks,
    convert_to_numpy=True,
    show_progress_bar=False)
    return embeddings.astype('float32')


def embed_query(query: str) -> np.ndarray:
    model = get_model()
    embedding = model.encode([query], convert_to_numpy=True)
    return embedding.astype('float32')