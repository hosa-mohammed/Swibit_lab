from fastapi import FastAPI
from app.core.database import Base, engine
from app.core.logging import logger
from app.api.routes import health, auth, tasks, audit
from fastapi.middleware.cors import CORSMiddleware

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

# CORS أولاً
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://10.57.159.196:8081",
        "http://192.168.128.1:8081",
        "http://host.docker.internal:8081",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ثم Routers
app.include_router(health.router, tags=["health"])
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(audit.router)