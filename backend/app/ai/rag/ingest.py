import os
from pathlib import Path


def load_documents(folder="docs/policies"):
    docs = []
    path = Path(folder)
    
    for file in path.glob("*.md"):
        text = file.read_text(encoding="utf-8")
        chunks = split_text(text, file.name)
        docs.extend(chunks)
    
    return docs


def split_text(text, filename, size=600, overlap=100):
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + size
        piece = text[start:end]

        if end < len(text):
            dot = piece.rfind(".")
            newline = piece.rfind("\n")
            cut = max(dot, newline)
            if cut > size * 0.5:
                end = start + cut + 1
                piece = text[start:end]

        heading = ""
        for line in piece.split("\n"):
            if line.startswith("#"):
                heading = line.strip("# ").strip()
                break
        
        chunks.append({
            "id": f"{filename}_{len(chunks)}",
            "text": piece.strip(),
            "source": filename,
            "heading": heading,
        })
        
        start = end - overlap
    
    return chunks


if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} chunks")
    for d in docs[:2]:
        print(f"\n--- {d['id']} ---")
        print(d['text'][:150])