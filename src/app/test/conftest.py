import pytest
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient

# Import the app and modules to patch
import src.app.main as main_module
from src.app.main import app
from src.app.db import validUser_mongo
from src.app.services import authServices

@pytest.fixture(scope="session", autouse=True)
def patch_lifespan():
    """
    Recreate Mongo objects in the test event loop.
    This avoids cross-loop AsyncMongoClient errors.
    """
    
    # Keep the original lifespan and wrap it.
    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def new_lifespan_wrapper(app_instance) -> AsyncGenerator[None, None]:
        # Build a fresh client inside the running test loop.
        new_client = AsyncMongoClient(validUser_mongo.MONGODB_URL)
        new_db = new_client[validUser_mongo.DB_NAME]
        
        # Repoint db globals to the test-loop client.
        old_client = validUser_mongo.client
        validUser_mongo.client = new_client
        validUser_mongo.db = new_db
        validUser_mongo.users_collection = new_db["users"]
        validUser_mongo.revoked_tokens_collection = new_db["revoked_tokens"]

        # main.py imported this symbol directly, so patch both places.
        validUser_mongo.close_mongo_connection = lambda: None
        main_module.close_mongo_connection = lambda: None

        # authServices also holds direct collection references.
        authServices.users_collection = validUser_mongo.users_collection
        authServices.revoked_tokens_collection = validUser_mongo.revoked_tokens_collection
        
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
