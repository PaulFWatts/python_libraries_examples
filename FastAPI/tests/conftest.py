"""
Pytest configuration and fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient

from main import Todo, app, todos_storage


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_todo_data():
    """Sample todo data for testing."""
    return {
        "title": "Test Todo",
        "description": "A test todo item",
        "priority": 3,
        "completed": False,
    }


@pytest.fixture
def sample_todo():
    """Create a sample Todo instance."""
    return Todo(
        title="Sample Todo",
        description="A sample todo for testing",
        priority=2,
        completed=False,
    )


@pytest.fixture(autouse=True)
def clear_todos_storage():
    """Clear todos storage before each test."""
    todos_storage.clear()
    yield
    todos_storage.clear()


@pytest.fixture
def populated_storage(sample_todo):
    """Populate storage with sample data for testing."""
    todos_storage.append(sample_todo)
    return sample_todo
