"""
Simple demonstration script showing FastAPI Todo API usage.

Run this after starting the main FastAPI application:
uv run python main.py

Then in another terminal:
uv run python examples/demo_usage.py
"""

import requests


def demo_api_usage():
    """Demonstrate API usage with simple requests."""
    base_url = "http://localhost:8000"

    print("🚀 FastAPI Demo Usage")
    print("=" * 30)

    try:
        # 1. Health check
        print("\n1. Health Check")
        response = requests.get(f"{base_url}/health")
        health_data = response.json()
        print(f"✅ API Status: {health_data['status']}")
        print(f"📊 Total Todos: {health_data['total_todos']}")

        # 2. Get initial todos
        print("\n2. Initial Todos")
        response = requests.get(f"{base_url}/todos")
        todos = response.json()
        print(f"📝 Found {len(todos)} existing todos")

        # 3. Create a new todo
        print("\n3. Creating New Todo")
        new_todo = {
            "title": "Demo Todo from Script",
            "description": "This todo was created via the demo script",
            "priority": 4,
            "completed": False,
        }

        response = requests.post(f"{base_url}/todos", json=new_todo)
        created_todo = response.json()
        todo_id = created_todo["id"]
        print(f"✅ Created: {created_todo['title']}")
        print(f"🆔 ID: {todo_id}")

        # 4. Update the todo
        print("\n4. Updating Todo")
        update_data = {
            "description": "Updated description from demo script",
            "priority": 5,
        }

        response = requests.put(f"{base_url}/todos/{todo_id}", json=update_data)
        updated_todo = response.json()
        print(f"📝 Updated priority to: {updated_todo['priority']}")

        # 5. Toggle completion
        print("\n5. Toggling Completion")
        response = requests.patch(f"{base_url}/todos/{todo_id}/toggle")
        toggled_todo = response.json()
        status_text = "completed" if toggled_todo["completed"] else "pending"
        print(f"🔄 Todo is now: {status_text}")

        # 6. Get statistics
        print("\n6. Getting Statistics")
        response = requests.get(f"{base_url}/todos/stats")
        stats = response.json()
        print(f"📊 Total: {stats['total_todos']}")
        print(f"✅ Completed: {stats['completed_todos']}")
        print(f"⏳ Pending: {stats['pending_todos']}")

        # 7. Filter todos
        print("\n7. Filtering Todos")
        response = requests.get(f"{base_url}/todos?priority=5")
        high_priority = response.json()
        print(f"🔥 High priority todos: {len(high_priority)}")

        response = requests.get(f"{base_url}/todos?completed=true")
        completed = response.json()
        print(f"✅ Completed todos: {len(completed)}")

        # 8. Get specific todo
        print("\n8. Getting Specific Todo")
        response = requests.get(f"{base_url}/todos/{todo_id}")
        specific_todo = response.json()
        print(f"📋 Retrieved: {specific_todo['title']}")

        print("\n🎉 Demo completed successfully!")
        print(f"\n📖 Visit {base_url}/docs for interactive API documentation")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to FastAPI server")
        print("Please start the server first: uv run python main.py")
    except Exception as e:
        print(f"❌ Error during demo: {e}")


if __name__ == "__main__":
    demo_api_usage()
