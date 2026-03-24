import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.app.api.auth import router as auth_router
from src.app.db.validUser_mongo import create_indexes, close_mongo_connection
from src.app.services.authServices import limiter


# @app.on_event is deprecated in modern FastAPI — use lifespan instead
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()
    yield
    close_mongo_connection()


app = FastAPI(lifespan=lifespan)

# CORS: allow the React dev server (and any origins set via env var) to reach the API
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
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