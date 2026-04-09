import os
import sys
from unittest.mock import AsyncMock, Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import src.app.main as main_module


def test_main_import_exposes_fastapi_app():
    assert isinstance(main_module.app, FastAPI)


def test_lifespan_hooks_run_without_crashing(monkeypatch):
    fake_create_indexes = AsyncMock()
    fake_close_connection = Mock()

    monkeypatch.setattr(main_module, "create_indexes", fake_create_indexes)
    monkeypatch.setattr(main_module, "close_mongo_connection", fake_close_connection)

    with TestClient(main_module.app) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
    fake_create_indexes.assert_awaited_once()
    fake_close_connection.assert_called_once()


def test_openapi_status_endpoint_returns_ok(monkeypatch):
    monkeypatch.setattr(main_module, "create_indexes", AsyncMock())
    monkeypatch.setattr(main_module, "close_mongo_connection", Mock())

    with TestClient(main_module.app) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json().get("openapi")
