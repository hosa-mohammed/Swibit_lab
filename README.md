# Swibit Lab

AI-powered task manager for small teams.

##  Overview

Swibit Lab is a full-stack task management application with an AI assistant. It includes a FastAPI backend, React Native mobile app, and intelligent document retrieval (RAG).

##  Project Structure


swibit-lab/
├── backend/          # FastAPI + AI/RAG
│   ├── app/
│   │   ├── ai/       # AI agent, classifier, RAG
│   │   ├── api/      # REST endpoints
│   │   └── core/     # Config, database
│   └── requirements.txt
├── mobile/           # React Native (Expo)
│   └── app/
│       ├── tasks.jsx
│       └── assistant.jsx
├── docker-compose.yml
└── eval/             # Evaluation scenarios


## 🛠️ Quick Start

### Docker (Recommended)

```bash
# 1. Set your OpenAI key
echo "LLM_API_KEY=sk-your-key" > .env

# 2. Run everything
docker-compose up --build