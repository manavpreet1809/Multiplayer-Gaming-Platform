import pytest
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient

# Import the app and modules to patch
import app.main as main_module
from app.main import app
from app.db import mongo as validUser_mongo
from app.db import usersRepo
from app.services import authServices

@pytest.fixture(scope="session", autouse=True)
def patch_lifespan():
    """
    Recreate Mongo objects in the test event loop.
    This avoids cross-loop AsyncMongoClient errors.
    """
    
    # Keep the original lifespan and wrap it.
    original_lifespan = app.router.lifespan_context

    # main.py awaits close_mongo_connection, but production function is sync.
    # Provide an async test stub; individual tests can still monkeypatch it.
    async def _test_close_mongo_connection():
        return None

    main_module.close_mongo_connection = _test_close_mongo_connection

    @asynccontextmanager
    async def new_lifespan_wrapper(app_instance) -> AsyncGenerator[None, None]:
        # Build a fresh client inside the running test loop.
        new_client = AsyncMongoClient(validUser_mongo.MONGODB_URL)
        new_db = new_client[validUser_mongo.DB_NAME]
        
        # Repoint db globals to the test-loop client.
        validUser_mongo.client = new_client
        validUser_mongo.db = new_db
        users_collection = new_db["users"]
        revoked_tokens_collection = new_db["revoked_tokens"]

        # usersRepo and authServices keep direct references to collections.
        usersRepo.users_collection = users_collection
        usersRepo.revoked_tokens_collection = revoked_tokens_collection
        authServices.users_collection = users_collection
        authServices.revoked_tokens_collection = revoked_tokens_collection

        try:
            # Run normal startup/shutdown work with patched objects.
            async with original_lifespan(app_instance) as state:
                yield state
        finally:
            # Close the test-loop client cleanly.
            await new_client.close()

    # Swap in the wrapper for tests.
    app.router.lifespan_context = new_lifespan_wrapper
    yield
