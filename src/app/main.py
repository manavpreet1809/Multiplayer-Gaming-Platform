from contextlib import asynccontextmanager

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from api.auth import router as auth_router
from db.validUser_mongo import create_indexes, close_mongo_connection
from src.app.services.authServices import limiter


# @app.on_event is deprecated in modern FastAPI — use lifespan instead
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()
    yield
    close_mongo_connection()


app = FastAPI(lifespan=lifespan)

# wire up the rate limiter and its 429 error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router)