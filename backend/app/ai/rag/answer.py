import json
import os
from openai import OpenAI
from app.ai.rag.retrieve import retrieve

client = OpenAI(api_key=os.environ.get("LLM_API_KEY", "test-key"))


def make_prompt(query, chunks):
    context = ""
    for c in chunks:
        context += f"\n[Source: {c['source']}, Section: {c['heading']}]\n{c['text']}\n"
    
    prompt = f"""You are a helpful assistant.
Answer using ONLY the provided documents.
Include citations with source file names.
If documents don't have the answer, say "I don't know".

Documents:{context}

Question: {query}

Answer in JSON:
{{
  "answer": "your answer",
  "citations": ["file.md"]
}}"""
    
    return prompt


def answer_question(query):
    chunks = retrieve(query, k=3)

    good = [c for c in chunks if c.get("score", 0) > 0.7]
    
    if not good:
        return {
            "answer": "I don't know",
            "citations": []
        }
    
    prompt = make_prompt(query, good)
    
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.3,
        timeout=30,
    )
    
    raw = resp.choices[0].message.content
    result = json.loads(raw)
    
    return {
        "answer": result.get("answer", "I don't know"),
        "citations": result.get("citations", [])
    }