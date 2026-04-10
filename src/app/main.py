import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.auth import router as auth_router
from app.api.games import router as games_router
from app.db.usersRepo import create_indexes, close_mongo_connection
from app.services.authServices import limiter


# @app.on_event is deprecated in modern FastAPI — use lifespan instead
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()
    yield
    await close_mongo_connection()


app = FastAPI(lifespan=lifespan)

# CORS: allow the React dev server (and any origins set via env var) to reach the API
ALLOWED_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# wire up the rate limiter and its 429 error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router)
app.include_router(games_router)