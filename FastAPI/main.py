"""
FastAPI Comprehensive Demo Application

This module demonstrates FastAPI's key features including:
- RESTful API endpoints with proper HTTP methods
- Pydantic models for request/response validation
- Async/await patterns for concurrent operations
- CORS middleware and request logging
- OpenAPI documentation generation
- Health check endpoints
- Error handling and custom exceptions
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator
from uvicorn import run

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Pydantic Models for Request/Response Validation
class TodoBase(BaseModel):
    """Base model for Todo items."""

    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: str | None = Field(
        None, max_length=1000, description="Detailed description"
    )
    priority: int = Field(1, ge=1, le=5, description="Priority level (1-5)")
    completed: bool = Field(False, description="Completion status")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Validate that title is not empty or just whitespace."""
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()


class TodoCreate(TodoBase):
    """Model for creating new Todo items."""

    pass


class TodoUpdate(BaseModel):
    """Model for updating existing Todo items."""

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    priority: int | None = Field(None, ge=1, le=5)
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str | None) -> str | None:
        """Validate that title is not empty or just whitespace."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v


class Todo(TodoBase):
    """Complete Todo model with metadata."""

    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime | None = Field(None, description="Last update timestamp")

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat(), UUID: lambda v: str(v)}
    )


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"
    total_todos: int


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str
    timestamp: datetime = Field(default_factory=datetime.now)


# In-memory storage (in production, use a proper database)
todos_storage: list[Todo] = []


# Custom exceptions
class TodoNotFoundError(HTTPException):
    """Exception raised when a todo item is not found."""

    def __init__(self, todo_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found",
        )


# Startup/shutdown event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    logger.info("🚀 FastAPI application starting up...")

    # Create some sample data
    sample_todos = [
        Todo(
            title="Learn FastAPI",
            description="Complete the FastAPI tutorial and build a demo application",
            priority=3,
            completed=False,
            updated_at=None,
        ),
        Todo(
            title="Write comprehensive tests",
            description="Implement unit and integration tests with pytest",
            priority=4,
            completed=True,
            updated_at=None,
        ),
        Todo(
            title="Deploy to production",
            description="Set up CI/CD pipeline and deploy the application",
            priority=5,
            completed=False,
            updated_at=None,
        ),
    ]
    todos_storage.extend(sample_todos)
    logger.info(f"📝 Initialized with {len(sample_todos)} sample todos")

    yield

    logger.info("🛑 FastAPI application shutting down...")


# Create FastAPI application with metadata
app = FastAPI(
    title="FastAPI Demo Application",
    description="""
    A comprehensive demonstration of FastAPI features including:

    * **RESTful API** with full CRUD operations
    * **Async/await patterns** for concurrent operations
    * **Pydantic validation** for request/response models
    * **OpenAPI documentation** with interactive Swagger UI
    * **CORS middleware** for cross-origin requests
    * **Request logging** and error handling
    * **Health check endpoints** for monitoring
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # In production, specify actual hosts
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    """Log all HTTP requests with timing information."""
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"📝 {request.method} {request.url.path} - "
        f"{response.status_code} - {process_time:.4f}s"
    )

    return response


# Helper functions
async def get_todo_by_id(todo_id: UUID) -> Todo:
    """Retrieve a todo by ID or raise 404."""
    for todo in todos_storage:
        if todo.id == todo_id:
            return todo
    raise TodoNotFoundError(todo_id)


async def simulate_async_operation() -> None:
    """Simulate an async operation (e.g., database call, API request)."""
    await asyncio.sleep(0.1)  # Simulate I/O operation


# API Routes


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check() -> HealthResponse:
    """
    Health check endpoint for monitoring and load balancers.

    Returns system status and basic metrics.
    """
    await simulate_async_operation()

    return HealthResponse(total_todos=len(todos_storage))


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    """Root endpoint with welcome message."""
    return {"message": "Welcome to FastAPI Demo!", "docs": "/docs", "health": "/health"}


@app.get("/todos", response_model=list[Todo], tags=["Todos"])
async def get_todos(
    completed: bool | None = Query(None, description="Filter by completion status"),
    priority: int | None = Query(
        None, ge=1, le=5, description="Filter by priority level"
    ),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of todos to return"
    ),
    skip: int = Query(0, ge=0, description="Number of todos to skip"),
) -> list[Todo]:
    """
    Retrieve todos with optional filtering and pagination.

    - **completed**: Filter by completion status (true/false)
    - **priority**: Filter by priority level (1-5)
    - **limit**: Maximum number of results (1-100)
    - **skip**: Number of results to skip for pagination
    """
    await simulate_async_operation()

    # Apply filters
    filtered_todos = todos_storage

    if completed is not None:
        filtered_todos = [
            todo for todo in filtered_todos if todo.completed == completed
        ]

    if priority is not None:
        filtered_todos = [todo for todo in filtered_todos if todo.priority == priority]

    # Apply pagination
    return filtered_todos[skip : skip + limit]


@app.get("/todos/stats", tags=["Analytics"])
async def get_todo_stats() -> dict[str, int]:
    """
    Get statistics about todos.

    Returns counts for total, completed, and pending todos by priority.
    """
    await simulate_async_operation()

    total = len(todos_storage)
    completed = len([todo for todo in todos_storage if todo.completed])
    pending = total - completed

    # Priority breakdown
    priority_stats = {}
    for priority in range(1, 6):
        count = len([todo for todo in todos_storage if todo.priority == priority])
        priority_stats[f"priority_{priority}"] = count

    return {
        "total_todos": total,
        "completed_todos": completed,
        "pending_todos": pending,
        **priority_stats,
    }


@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def get_todo(todo_id: UUID) -> Todo:
    """
    Retrieve a specific todo by ID.

    Returns the todo item if found, otherwise returns 404.
    """
    await simulate_async_operation()
    return await get_todo_by_id(todo_id)


@app.post(
    "/todos", response_model=Todo, status_code=status.HTTP_201_CREATED, tags=["Todos"]
)
async def create_todo(todo: TodoCreate) -> Todo:
    """
    Create a new todo item.

    The todo will be assigned a unique ID and timestamp automatically.
    """
    await simulate_async_operation()

    new_todo = Todo(**todo.model_dump())
    todos_storage.append(new_todo)

    logger.info(f"✅ Created new todo: {new_todo.title} (ID: {new_todo.id})")
    return new_todo


@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def update_todo(todo_id: UUID, todo_update: TodoUpdate) -> Todo:
    """
    Update an existing todo item.

    Only provided fields will be updated. The updated_at timestamp
    will be automatically set to the current time.
    """
    await simulate_async_operation()

    existing_todo = await get_todo_by_id(todo_id)

    # Update only provided fields
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_todo, field, value)

    existing_todo.updated_at = datetime.now()

    logger.info(f"📝 Updated todo: {existing_todo.title} (ID: {todo_id})")
    return existing_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"])
async def delete_todo(todo_id: UUID) -> None:
    """
    Delete a todo item by ID.

    Returns 204 No Content on successful deletion.
    """
    await simulate_async_operation()

    todo_to_delete = await get_todo_by_id(todo_id)
    todos_storage.remove(todo_to_delete)

    logger.info(f"🗑️ Deleted todo: {todo_to_delete.title} (ID: {todo_id})")


@app.patch("/todos/{todo_id}/toggle", response_model=Todo, tags=["Todos"])
async def toggle_todo_completion(todo_id: UUID) -> Todo:
    """
    Toggle the completion status of a todo item.

    This is a convenience endpoint for quickly marking todos as done/undone.
    """
    await simulate_async_operation()

    todo = await get_todo_by_id(todo_id)
    todo.completed = not todo.completed
    todo.updated_at = datetime.now()

    status_text = "completed" if todo.completed else "reopened"
    logger.info(f"🔄 {status_text.title()} todo: {todo.title} (ID: {todo_id})")

    return todo


# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors with custom response."""
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


if __name__ == "__main__":
    """Run the application with uvicorn."""
    logger.info("🚀 Starting FastAPI Demo Application...")

    run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
