import ollama
import json
from typing import Generator
import os

CLASSIFIER_SYSTEM_PROMPT = """You are a message classifier for a Task Management system.
Analyze the user's message and classify it into the correct category.
Always respond with valid JSON only. No extra text.

## JSON Schema

{
  "category": "sales | support | billing | complaint | general",
  "priority": "low | medium | high",
  "summary": "string",
  "suggested_action": "string"
}

## Rules

- sales: Questions about pricing, plans, subscriptions, upgrades
- support: Technical issues, bugs, errors, how-to questions
- billing: Payments, invoices, refunds, charges
- complaint: Negative feedback, service complaints, demands
- general: Greetings, thanks, unrelated messages

- priority high: Urgent words like "urgent", "asap", "immediately", "down", "broken"
- priority medium: Normal requests without urgency
- priority low: General inquiries, non-urgent questions
"""


EXTRACTOR_SYSTEM_PROMPT = """You are an information extractor for a Task Management system.
Extract structured fields from the user's unstructured message.
Always respond with valid JSON only. No extra text.

## JSON Schema

{
  "requester_name": "string | null",
  "request_type": "new_task | update | question",
  "urgency": "low | medium | high",
  "task_title_guess": "string | null"
}

## Rules

- requester_name: Extract the person's name if mentioned. If no name found, use null.
- request_type:
  - new_task: Creating something new, adding features
  - update: Changes to existing tasks
  - question: Asking about status, how-to, when
- urgency:
  - high: "urgent", "asap", "immediately", "critical", "down", "broken"
  - low: "when you have time", "no rush", "later"
  - medium: Everything else
- task_title_guess: Create a short task title (3-6 words). If unclear, use null.
"""


RAG_SYSTEM_PROMPT = """You are a Task Management AI Assistant. You help users manage their tasks intelligently.

You have access to the user's actual tasks from the database. Use ONLY the provided context to answer.
If the context doesn't contain the answer, say "I don't see that in your tasks."

Always respond in the same language as the user's question (Arabic or English).

## Context (User's Tasks):
{context}

## User Question: {question}

## Instructions:
1. Answer based ONLY on the context above
2. Be concise but helpful
3. If asking about priorities, list tasks in order
4. If asking about deadlines, mention dates clearly
5. If no relevant tasks found, say so politely

Answer:"""

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = ollama.Client(host=OLLAMA_HOST)

def call_llama(system: str, user: str, stream: bool = False, temperature: float = 0.3):
    """استدعاء Llama 3.2"""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]
    
    if stream:
        return ollama.chat(
            model='llama3.2',
            messages=messages,
            stream=True,
            options={"temperature": temperature, "num_predict": 500}
        )
    
    response = ollama.chat(
        model='llama3.2',
        messages=messages,
        options={"temperature": temperature, "num_predict": 500}
    )
    return response['message']['content']


def classify_message(message: str) -> dict:
    """Prompt 1: Message Classifier"""
    raw = call_llama(CLASSIFIER_SYSTEM_PROMPT, message)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "category": "general",
            "priority": "medium",
            "summary": message[:50],
            "suggested_action": "Review manually"
        }


def extract_info(message: str) -> dict:
    """Prompt 2: Information Extractor"""
    raw = call_llama(EXTRACTOR_SYSTEM_PROMPT, message)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "requester_name": None,
            "request_type": "question",
            "urgency": "medium",
            "task_title_guess": None
        }


def rag_answer(question: str, context_chunks: list[dict]) -> str:
    """Prompt 3: RAG Answer (الجديد)"""
    # دمج الـ chunks كسياق
    context = "\n\n".join([
        f"[{i+1}] {chunk['text']}"
        for i, chunk in enumerate(context_chunks)
    ])
    
    prompt = RAG_SYSTEM_PROMPT.format(context=context, question=question)
    
    # لا system prompt منفصل - الكل في user message (Llama يفضل هذا)
    return call_llama("", prompt, temperature=0.3)


def rag_answer_stream(question: str, context_chunks: list[dict]) -> Generator[str, None, None]:
    """RAG Answer مع Streaming"""
    context = "\n\n".join([
        f"[{i+1}] {chunk['text']}"
        for i, chunk in enumerate(context_chunks)
    ])
    
    prompt = RAG_SYSTEM_PROMPT.format(context=context, question=question)
    
    stream = call_llama("", prompt, stream=True, temperature=0.3)
    
    for chunk in stream:
        yield chunk['message']['content']