from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.routes import health, auth, tasks


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Swibit Lab API",
    version="0.3.0",
    description="Task manager backend — Week 4",
)

app.include_router(health.router, tags=["health"])
app.include_router(auth.router)
app.include_router(tasks.router)