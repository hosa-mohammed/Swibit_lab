from fastapi import FastAPI
from app.api.routes import health

app = FastAPI(
    title="Swibit Lab API",
    version="0.1.0",
    description="Task manager backend — Week 3",
)

app.include_router(health.router, tags=["health"])


@app.get("/")
def root():
    return {"message": "Swibit Lab API v0.1"}