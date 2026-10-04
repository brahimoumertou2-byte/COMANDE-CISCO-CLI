from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, SessionLocal, engine
from .routers import categories, commands, generator, search, troubleshooting
from .services.command_service import seed_commands


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_commands(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Cisco CLI Command Center",
    version="1.0.0",
    description="Search, explain, generate and troubleshoot Cisco IOS-style CLI commands.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(commands.router)
app.include_router(categories.router)
app.include_router(search.router)
app.include_router(generator.router)
app.include_router(troubleshooting.router)


@app.get("/")
def root():
    return {"name": "Cisco CLI Command Center", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}
