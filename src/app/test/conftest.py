import os

# Must run before app.services.authServices (imported via app.main) reads SECRET_KEY.
if not os.environ.get("SECRET_KEY") or os.environ.get("SECRET_KEY") == "CHANGE_ME_TO_A_LONG_RANDOM_SECRET":
    os.environ["SECRET_KEY"] = "pytest-only-secret-key-do-not-use-in-production-0123456789ab"

import pytest
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient

import app.services.authServices as auth_services

# Before app.main loads route modules, neutralize SlowAPI (many logins → 429 otherwise).
auth_services.limiter.limit = lambda *args, **kwargs: (lambda f: f)

from app.main import app
from app.db import mongo as mongo_mod
from app.db import usersRepo
from app.services import authServices


@pytest.fixture(scope="session", autouse=True)
def patch_lifespan():
    """
    Patch the FastAPI lifespan to re-initialize the MongoDB client
    inside the event loop that TestClient/FastAPI runs in.
    This fixes 'RuntimeError: Cannot use AsyncMongoClient in different event loop'.
    """
    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def new_lifespan_wrapper(app_instance) -> AsyncGenerator[None, None]:
        new_client = AsyncMongoClient(mongo_mod.MONGODB_URL)
        new_db = new_client[mongo_mod.DB_NAME]

        old_client = mongo_mod.client
        mongo_mod.client = new_client
        mongo_mod.db = new_db

        usersRepo.users_collection = new_db["users"]
        usersRepo.revoked_tokens_collection = new_db["revoked_tokens"]

        async def _noop():
            pass

        mongo_mod.close_mongo_connection = _noop
        usersRepo.close_mongo_connection = _noop
        import app.main as main_mod

        main_mod.close_mongo_connection = _noop

        authServices.users_collection = usersRepo.users_collection
        authServices.revoked_tokens_collection = usersRepo.revoked_tokens_collection

        try:
            async with original_lifespan(app_instance) as state:
                yield state
        finally:
            mongo_mod.client = old_client
            await new_client.close()

    app.router.lifespan_context = new_lifespan_wrapper
    yield
