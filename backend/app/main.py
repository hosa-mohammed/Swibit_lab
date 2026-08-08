from fastapi import FastAPI
from app.core.database import Base, engine
from app.core.logging import logger
from app.api.routes import health, auth, tasks, audit  

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Swibit Lab API",
    version="1.0.0",
    description="Task manager backend — Week 5 (v1.0)",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up", extra={"version": "1.0.0"})

app.include_router(health.router, tags=["health"])
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(audit.router) 