# FastAPI Demo Application

A comprehensive demonstration of **FastAPI** features showcasing modern Python web development patterns with async/await, automatic API documentation, and robust validation.

## 🚀 Quick Start

```bash
# Install dependencies
uv sync

# Run the application
uv run python main.py

# Visit the interactive API docs
# http://localhost:8000/docs
```

## 🎮 Running Examples

This demo includes two example scripts demonstrating different approaches to API interaction:

### Option 1: Simple Synchronous Demo
```bash
# Terminal 1: Start the FastAPI server
uv run python main.py

# Terminal 2: Run the demo script (in another terminal)
uv run python examples/demo_usage.py
```

### Option 2: Advanced Async Client Demo
```bash
# Terminal 1: Start the FastAPI server
uv run python main.py

# Terminal 2: Run the async client demo (in another terminal)
uv run python examples/client_demo.py
```

**Note**: The server must be running before executing either example script. The examples will demonstrate creating, updating, filtering, and deleting todos through the API.

## 📋 Features Demonstrated

### Core FastAPI Features
- **RESTful API Design** - Full CRUD operations for Todo management
- **Automatic API Documentation** - Interactive Swagger UI and ReDoc
- **Pydantic Validation** - Request/response model validation with custom validators
- **Async/Await Patterns** - Concurrent request handling and I/O operations
- **Type Hints** - Modern Python type annotations throughout

### Middleware & Cross-Cutting Concerns
- **CORS Middleware** - Cross-origin resource sharing configuration
- **Request Logging** - Structured logging with timing information
- **Trusted Host Middleware** - Security middleware for production
- **Custom Exception Handling** - Global error handling patterns

### Advanced Patterns
- **Lifespan Events** - Application startup/shutdown with sample data
- **Query Parameters** - Filtering, pagination, and validation
- **Path Parameters** - UUID validation and routing
- **Response Models** - Typed responses with metadata
- **Custom Validators** - Business logic validation in Pydantic models

## 🏗️ API Endpoints

### System Endpoints
- `GET /` - Welcome message with navigation links
- `GET /health` - Health check with system metrics
- `GET /docs` - Interactive Swagger UI documentation
- `GET /redoc` - Alternative ReDoc documentation

### Todo Management
- `GET /todos` - List todos with filtering and pagination
  - Query params: `completed`, `priority`, `limit`, `skip`
- `POST /todos` - Create new todo item
- `GET /todos/{id}` - Get specific todo by UUID
- `PUT /todos/{id}` - Update existing todo
- `DELETE /todos/{id}` - Delete todo item
- `PATCH /todos/{id}/toggle` - Toggle completion status

### Analytics
- `GET /todos/stats` - Get todo statistics and priority breakdown

## 📊 Data Models

### TodoBase
```python
class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    priority: int = Field(1, ge=1, le=5)
    completed: bool = Field(False)
```

### Todo (Complete Model)
Extends TodoBase with:
- `id: UUID` - Unique identifier
- `created_at: datetime` - Creation timestamp
- `updated_at: datetime | None` - Last update timestamp

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests with coverage (recommended)
uv run python -m pytest tests/ -v --cov=main

# Alternative: Run with direct Python interpreter
.\.venv\Scripts\python.exe -m pytest tests/ -v --cov=main

# Run specific test categories
uv run python -m pytest tests/test_main.py::TestTodosCRUD -v

# Generate HTML coverage report
uv run python -m pytest tests/ --cov=main --cov-report=html
```

### Test Categories
- **CRUD Operations** - Create, read, update, delete functionality
- **Validation Testing** - Pydantic model validation edge cases
- **Filtering & Pagination** - Query parameter handling
- **Error Handling** - 404s, validation errors, edge cases
- **Async Behavior** - Concurrent request handling
- **OpenAPI Documentation** - Schema generation and UI accessibility

## 🔧 Development Commands

```bash
# Format code
uv run black .
uv run isort .

# Lint code
uv run ruff check

# Type checking
uv run mypy .

# Run with auto-reload for development
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Usage Examples

### Creating a Todo
```bash
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the comprehensive tutorial",
    "priority": 4,
    "completed": false
  }'
```

### Filtering Todos
```bash
# Get only completed todos
curl "http://localhost:8000/todos?completed=true"

# Get high priority todos
curl "http://localhost:8000/todos?priority=5"

# Pagination
curl "http://localhost:8000/todos?limit=5&skip=10"
```

### Getting Statistics
```bash
curl "http://localhost:8000/todos/stats"
```

## 🏭 Production Considerations

This demo includes production-ready patterns:

### Security
- CORS middleware configuration
- Trusted host middleware
- Input validation with Pydantic
- UUID-based resource identification

### Monitoring
- Health check endpoint for load balancers
- Structured logging with request timing
- Statistics endpoint for metrics collection

### Performance
- Async/await for concurrent operations
- Efficient filtering and pagination
- Minimal memory footprint with in-memory storage

### API Design
- RESTful conventions
- Proper HTTP status codes
- Comprehensive error responses
- OpenAPI 3.0 specification compliance

## 🎯 Learning Objectives

After exploring this demo, you'll understand:

1. **FastAPI Fundamentals** - Route definition, dependency injection, middleware
2. **Pydantic Integration** - Model validation, serialization, custom validators
3. **Async Programming** - Event loops, concurrent operations, async/await patterns
4. **API Design** - RESTful principles, proper status codes, error handling
5. **Testing Strategies** - Unit tests, integration tests, async testing
6. **Documentation** - Automatic OpenAPI generation, interactive docs

## 📚 Further Reading

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)

---

This demonstration showcases FastAPI as a modern, high-performance web framework ideal for building APIs with automatic documentation, type safety, and excellent developer experience.
