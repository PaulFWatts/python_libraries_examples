"""
Comprehensive tests for the FastAPI Todo application.
"""

from uuid import uuid4

import pytest
from fastapi import status


class TestHealthEndpoint:
    """Test health check functionality."""

    def test_health_check(self, client):
        """Test health endpoint returns correct status."""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data
        assert "total_todos" in data


class TestRootEndpoint:
    """Test root endpoint functionality."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns welcome message."""
        response = client.get("/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["message"] == "Welcome to FastAPI Demo!"
        assert data["docs"] == "/docs"
        assert data["health"] == "/health"


class TestTodosCRUD:
    """Test Todo CRUD operations."""

    def test_get_empty_todos(self, client):
        """Test getting todos when storage is empty."""
        response = client.get("/todos")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_todo(self, client, sample_todo_data):
        """Test creating a new todo."""
        response = client.post("/todos", json=sample_todo_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["title"] == sample_todo_data["title"]
        assert data["description"] == sample_todo_data["description"]
        assert data["priority"] == sample_todo_data["priority"]
        assert data["completed"] == sample_todo_data["completed"]
        assert "id" in data
        assert "created_at" in data

    def test_create_todo_validation_error(self, client):
        """Test creating todo with validation errors."""
        invalid_data = {
            "title": "",  # Empty title should fail
            "priority": 10,  # Priority > 5 should fail
        }

        response = client.post("/todos", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_todo_by_id(self, client, populated_storage):
        """Test retrieving a specific todo by ID."""
        todo_id = str(populated_storage.id)
        response = client.get(f"/todos/{todo_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["id"] == todo_id
        assert data["title"] == populated_storage.title

    def test_get_nonexistent_todo(self, client):
        """Test retrieving a todo that doesn't exist."""
        fake_id = str(uuid4())
        response = client.get(f"/todos/{fake_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_todo(self, client, populated_storage):
        """Test updating an existing todo."""
        todo_id = str(populated_storage.id)
        update_data = {"title": "Updated Title", "completed": True}

        response = client.put(f"/todos/{todo_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["title"] == "Updated Title"
        assert data["completed"] is True
        assert "updated_at" in data

    def test_update_nonexistent_todo(self, client):
        """Test updating a todo that doesn't exist."""
        fake_id = str(uuid4())
        update_data = {"title": "Updated Title"}

        response = client.put(f"/todos/{fake_id}", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_todo(self, client, populated_storage):
        """Test deleting an existing todo."""
        todo_id = str(populated_storage.id)

        response = client.delete(f"/todos/{todo_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify todo is deleted
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_todo(self, client):
        """Test deleting a todo that doesn't exist."""
        fake_id = str(uuid4())

        response = client.delete(f"/todos/{fake_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_toggle_todo_completion(self, client, populated_storage):
        """Test toggling todo completion status."""
        todo_id = str(populated_storage.id)
        original_status = populated_storage.completed

        response = client.patch(f"/todos/{todo_id}/toggle")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["completed"] != original_status
        assert "updated_at" in data


class TestTodosFiltering:
    """Test todo filtering and pagination."""

    def test_filter_by_completion_status(self, client):
        """Test filtering todos by completion status."""
        # Create test todos
        completed_todo = {"title": "Completed Todo", "completed": True}
        pending_todo = {"title": "Pending Todo", "completed": False}

        client.post("/todos", json=completed_todo)
        client.post("/todos", json=pending_todo)

        # Test filtering completed todos
        response = client.get("/todos?completed=true")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["completed"] is True

        # Test filtering pending todos
        response = client.get("/todos?completed=false")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["completed"] is False

    def test_filter_by_priority(self, client):
        """Test filtering todos by priority level."""
        # Create todos with different priorities
        high_priority = {"title": "High Priority", "priority": 5}
        low_priority = {"title": "Low Priority", "priority": 1}

        client.post("/todos", json=high_priority)
        client.post("/todos", json=low_priority)

        # Test filtering by priority
        response = client.get("/todos?priority=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["priority"] == 5

    def test_pagination(self, client):
        """Test todo pagination."""
        # Create multiple todos
        for i in range(15):
            todo_data = {"title": f"Todo {i}", "priority": 1}
            client.post("/todos", json=todo_data)

        # Test default limit
        response = client.get("/todos")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 10  # Default limit

        # Test custom limit and skip
        response = client.get("/todos?limit=5&skip=10")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 5


class TestTodoStats:
    """Test todo statistics endpoint."""

    def test_get_stats_empty(self, client):
        """Test stats with empty storage."""
        response = client.get("/todos/stats")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["total_todos"] == 0
        assert data["completed_todos"] == 0
        assert data["pending_todos"] == 0

    def test_get_stats_with_data(self, client):
        """Test stats with sample data."""
        # Create test todos
        todos = [
            {"title": "Todo 1", "priority": 1, "completed": True},
            {"title": "Todo 2", "priority": 2, "completed": False},
            {"title": "Todo 3", "priority": 1, "completed": False},
        ]

        for todo in todos:
            client.post("/todos", json=todo)

        response = client.get("/todos/stats")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["total_todos"] == 3
        assert data["completed_todos"] == 1
        assert data["pending_todos"] == 2
        assert data["priority_1"] == 2
        assert data["priority_2"] == 1


class TestValidation:
    """Test Pydantic model validation."""

    def test_title_validation(self, client):
        """Test title field validation."""
        # Test empty title
        response = client.post("/todos", json={"title": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Test whitespace-only title
        response = client.post("/todos", json={"title": "   "})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Test title too long
        long_title = "x" * 201
        response = client.post("/todos", json={"title": long_title})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_priority_validation(self, client):
        """Test priority field validation."""
        # Test priority too low
        response = client.post("/todos", json={"title": "Test", "priority": 0})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Test priority too high
        response = client.post("/todos", json={"title": "Test", "priority": 6})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Test valid priority
        response = client.post("/todos", json={"title": "Test", "priority": 3})
        assert response.status_code == status.HTTP_201_CREATED


class TestAsyncBehavior:
    """Test async behavior and concurrent operations."""

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client):
        """Test handling multiple concurrent requests."""

        # Create multiple todos concurrently using the sync client
        def create_todo_sync(i):
            todo_data = {"title": f"Concurrent Todo {i}", "priority": 1}
            return client.post("/todos", json=todo_data)

        # Create todos concurrently (simulating concurrent requests)
        responses = []
        for i in range(5):
            response = create_todo_sync(i)
            responses.append(response)

        # All requests should succeed
        for response in responses:
            assert response.status_code == status.HTTP_201_CREATED

        # Verify all todos were created
        response = client.get("/todos")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 5


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_invalid_uuid_format(self, client):
        """Test invalid UUID format in path parameters."""
        response = client.get("/todos/invalid-uuid")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_invalid_query_parameters(self, client):
        """Test invalid query parameters."""
        # Invalid priority range
        response = client.get("/todos?priority=10")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Invalid limit
        response = client.get("/todos?limit=0")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Invalid skip
        response = client.get("/todos?skip=-1")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestOpenAPIDocumentation:
    """Test OpenAPI documentation endpoints."""

    def test_openapi_schema(self, client):
        """Test OpenAPI schema generation."""
        response = client.get("/openapi.json")
        assert response.status_code == status.HTTP_200_OK

        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "FastAPI Demo Application"

    def test_swagger_ui(self, client):
        """Test Swagger UI accessibility."""
        response = client.get("/docs")
        assert response.status_code == status.HTTP_200_OK

    def test_redoc_ui(self, client):
        """Test ReDoc UI accessibility."""
        response = client.get("/redoc")
        assert response.status_code == status.HTTP_200_OK
