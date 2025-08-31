"""
FastAPI Client Example

This script demonstrates how to interact with the FastAPI Todo application
programmatically using the httpx library for async HTTP requests.
"""

import asyncio
from datetime import datetime
from uuid import UUID

import httpx


class TodoClient:
    """Async client for interacting with the FastAPI Todo application."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def health_check(self) -> dict:
        """Check if the API is healthy."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()

    async def create_todo(
        self,
        title: str,
        description: str = None,
        priority: int = 1,
        completed: bool = False,
    ) -> dict:
        """Create a new todo item."""
        todo_data = {
            "title": title,
            "description": description,
            "priority": priority,
            "completed": completed,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/todos", json=todo_data)
            response.raise_for_status()
            return response.json()

    async def get_todos(
        self,
        completed: bool = None,
        priority: int = None,
        limit: int = 10,
        skip: int = 0,
    ) -> list[dict]:
        """Get todos with optional filtering."""
        params = {"limit": limit, "skip": skip}

        if completed is not None:
            params["completed"] = completed
        if priority is not None:
            params["priority"] = priority

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/todos", params=params)
            response.raise_for_status()
            return response.json()

    async def get_todo(self, todo_id: UUID) -> dict:
        """Get a specific todo by ID."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/todos/{todo_id}")
            response.raise_for_status()
            return response.json()

    async def update_todo(self, todo_id: UUID, **updates) -> dict:
        """Update an existing todo."""
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/todos/{todo_id}", json=updates
            )
            response.raise_for_status()
            return response.json()

    async def delete_todo(self, todo_id: UUID) -> bool:
        """Delete a todo item."""
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.base_url}/todos/{todo_id}")
            return response.status_code == 204

    async def toggle_todo(self, todo_id: UUID) -> dict:
        """Toggle the completion status of a todo."""
        async with httpx.AsyncClient() as client:
            response = await client.patch(f"{self.base_url}/todos/{todo_id}/toggle")
            response.raise_for_status()
            return response.json()

    async def get_stats(self) -> dict:
        """Get todo statistics."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/todos/stats")
            response.raise_for_status()
            return response.json()


async def demo_workflow():
    """Demonstrate a complete workflow using the Todo API."""
    client = TodoClient()

    print("🚀 FastAPI Client Demo Workflow")
    print("=" * 40)

    # 1. Check API health
    print("\n1. Checking API health...")
    health = await client.health_check()
    print(f"✅ API Status: {health['status']}")
    print(f"📊 Total Todos: {health['total_todos']}")

    # 2. Create some todos
    print("\n2. Creating todos...")
    todos_to_create = [
        {
            "title": "Set up development environment",
            "description": "Install Python, UV, and FastAPI",
            "priority": 5,
            "completed": True,
        },
        {
            "title": "Build Todo API",
            "description": "Create a comprehensive FastAPI application",
            "priority": 4,
            "completed": False,
        },
        {
            "title": "Write comprehensive tests",
            "description": "Implement unit and integration tests",
            "priority": 3,
            "completed": False,
        },
    ]

    created_todos = []
    for todo_data in todos_to_create:
        todo = await client.create_todo(**todo_data)
        created_todos.append(todo)
        print(f"✅ Created: {todo['title']} (ID: {todo['id']})")

    # 3. List all todos
    print("\n3. Listing all todos...")
    all_todos = await client.get_todos()
    print(f"📝 Found {len(all_todos)} todos total")

    # 4. Filter todos
    print("\n4. Filtering todos...")
    completed_todos = await client.get_todos(completed=True)
    print(f"✅ Completed todos: {len(completed_todos)}")

    high_priority_todos = await client.get_todos(priority=5)
    print(f"🔥 High priority todos: {len(high_priority_todos)}")

    # 5. Update a todo
    print("\n5. Updating a todo...")
    todo_to_update = created_todos[1]  # The "Build Todo API" todo
    updated_todo = await client.update_todo(
        UUID(todo_to_update["id"]),
        description="Create a production-ready FastAPI application with tests",
        priority=5,
    )
    print(f"📝 Updated: {updated_todo['title']}")
    print(f"   New priority: {updated_todo['priority']}")

    # 6. Toggle completion
    print("\n6. Toggling todo completion...")
    toggled_todo = await client.toggle_todo(UUID(todo_to_update["id"]))
    status = "completed" if toggled_todo["completed"] else "pending"
    print(f"🔄 Toggled todo to: {status}")

    # 7. Get statistics
    print("\n7. Getting statistics...")
    stats = await client.get_stats()
    print(f"📊 Total: {stats['total_todos']}")
    print(f"✅ Completed: {stats['completed_todos']}")
    print(f"⏳ Pending: {stats['pending_todos']}")

    for priority in range(1, 6):
        count = stats.get(f"priority_{priority}", 0)
        if count > 0:
            print(f"🎯 Priority {priority}: {count} todos")

    # 8. Get specific todo
    print("\n8. Getting specific todo...")
    specific_todo = await client.get_todo(UUID(created_todos[0]["id"]))
    print(f"📋 Retrieved: {specific_todo['title']}")

    # 9. Delete a todo
    print("\n9. Deleting a todo...")
    success = await client.delete_todo(UUID(created_todos[2]["id"]))
    if success:
        print(f"🗑️ Deleted: {created_todos[2]['title']}")

    # 10. Final statistics
    print("\n10. Final statistics...")
    final_stats = await client.get_stats()
    print(f"📊 Final total: {final_stats['total_todos']} todos")

    print("\n🎉 Demo workflow completed successfully!")


async def concurrent_operations_demo():
    """Demonstrate concurrent API operations."""
    client = TodoClient()

    print("\n🔄 Concurrent Operations Demo")
    print("=" * 35)

    # Create multiple todos concurrently
    tasks = []
    for i in range(5):
        task = client.create_todo(
            title=f"Concurrent Todo {i + 1}",
            description=f"Todo created concurrently #{i + 1}",
            priority=(i % 5) + 1,
        )
        tasks.append(task)

    print("⚡ Creating 5 todos concurrently...")
    start_time = datetime.now()
    results = await asyncio.gather(*tasks)
    end_time = datetime.now()

    duration = (end_time - start_time).total_seconds()
    print(f"✅ Created {len(results)} todos in {duration:.2f} seconds")

    # Get stats to verify
    stats = await client.get_stats()
    print(f"📊 Total todos in system: {stats['total_todos']}")


if __name__ == "__main__":
    print("🚀 Starting FastAPI Client Demo")
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("Run: uv run python main.py")
    print()

    try:
        # Run the main demo workflow
        asyncio.run(demo_workflow())

        # Run concurrent operations demo
        asyncio.run(concurrent_operations_demo())

    except httpx.ConnectError:
        print("❌ Could not connect to FastAPI server")
        print("Please start the server first: uv run python main.py")
    except Exception as e:
        print(f"❌ Error during demo: {e}")
