import pytest
import asyncio
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from unittest.mock import MagicMock
from pymongo import AsyncMongoClient

# Import the app and modules to patch
from app.main import app
from app.db import validUser_mongo
from app.services import authServices

@pytest.fixture(scope="session", autouse=True)
def patch_lifespan():
    """
    Patch the FastAPI lifespan to re-initialize the MongoDB client
    inside the event loop that TestClient/FastAPI runs in.
    This is to fix 'RuntimeError: Cannot use AsyncMongoClient in different event loop'
    This error comes up if tests ran without re-initializing the MongoDB client.
    """
    
    # Store the original lifespan context manager
    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def new_lifespan_wrapper(app_instance) -> AsyncGenerator[None, None]:
        # We are now inside the correct running loop.
        
        # 1. Initialize a new AsyncMongoClient in this loop
        #    Use the same URL and DB name from the module
        new_client = AsyncMongoClient(validUser_mongo.MONGODB_URL)
        new_db = new_client[validUser_mongo.DB_NAME]
        
        # 2. Patch the module-level variables in validUser_mongo
        #    so that create_indexes and other functions use the new client.
        old_client = validUser_mongo.client
        validUser_mongo.client = new_client
        validUser_mongo.db = new_db
        validUser_mongo.users_collection = new_db["users"]
        validUser_mongo.revoked_tokens_collection = new_db["revoked_tokens"]

        # Patch close_mongo_connection to be a no-op, since we close it manually
        # and the original function is synchronous which causes a RuntimeWarning
        # We must overwrite it in both validUser_mongo (source) and main (where it's imported)
        validUser_mongo.close_mongo_connection = lambda: None
        import app.main
        app.main.close_mongo_connection = lambda: None
        
        # 3. Patch authServices because it imports these collections directly
        authServices.users_collection = validUser_mongo.users_collection
        authServices.revoked_tokens_collection = validUser_mongo.revoked_tokens_collection
        
        try:
            # 4. Delegate to the original lifespan (which calls create_indexes)
            async with original_lifespan(app_instance) as state:
                yield state
        finally:
            # 5. Cleanup
            # Note: validUser_mongo.close_mongo_connection() in main.py tries to close the client too,
            # but usually fails to await it. We ensure proper closure here.
            await new_client.close()

    # Apply the patch
    app.router.lifespan_context = new_lifespan_wrapper
    yield
