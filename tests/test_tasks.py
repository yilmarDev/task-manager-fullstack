import pytest
from httpx import AsyncClient
from uuid import uuid4
from datetime import datetime, timezone, timedelta


class TestCreateTask:
    """Test suite for task creation endpoint"""

    @pytest.mark.asyncio
    async def test_create_task_success(self, client: AsyncClient, test_user):
        """Test successful task creation"""
        response = await client.post(
            "/api/tasks",
            json={
                "title": "Complete project",
                "description": "Finish the API implementation",
                "due_date": (
                    datetime.now(timezone.utc) + timedelta(days=7)
                ).isoformat(),
            },
            params={"owner_id": str(test_user.id)},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Complete project"
        assert data["description"] == "Finish the API implementation"
        assert data["status"] == "pending"
        assert data["owner_id"] == str(test_user.id)
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_task_invalid_assignee(self, client: AsyncClient, test_user):
        """Test creating task with invalid assignee UUID raises ValueError"""
        response = await client.post(
            "/api/tasks",
            params={"owner_id": str(test_user.id)},
            json={
                "title": "Test Task",
                "description": "Task with invalid assignee",
                "assigned_to_id": "00000000-0000-0000-0000-000000000000",  # Non-existent UUID
            },
        )

        assert response.status_code == 400
        assert "user not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_task_missing_title(self, client: AsyncClient, test_user):
        """Test task creation fails without title"""
        response = await client.post(
            "/api/tasks",
            json={
                "description": "Missing title",
            },
            params={"owner_id": str(test_user.id)},
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_task_optional_fields(self, client: AsyncClient, test_user):
        """Test task creation with only required fields"""
        response = await client.post(
            "/api/tasks",
            json={"title": "Simple task"},
            params={"owner_id": str(test_user.id)},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Simple task"
        assert data["description"] is None
        assert data["due_date"] is None
        assert "owner_id" in data

    @pytest.mark.asyncio
    async def test_create_task_with_assignee(self, client: AsyncClient, test_user):
        """Test creating task assigned to another user"""
        # Create another user
        user2_response = await client.post(
            "/api/users",
            json={
                "name": "User Two",
                "email": "user2@example.com",
                "password": "pass123",
            },
        )
        user2_id = user2_response.json()["id"]

        response = await client.post(
            "/api/tasks",
            json={
                "title": "Assigned task",
                "assigned_to_id": user2_id,
            },
            params={"owner_id": str(test_user.id)},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["assigned_to_id"] == user2_id


class TestGetTask:
    """Test suite for get task endpoint"""

    @pytest.mark.asyncio
    async def test_get_task_success_as_owner(
        self, client: AsyncClient, test_user, test_task
    ):
        """Test retrieving a task as the owner"""
        response = await client.get(
            f"/api/tasks/{test_task.id}",
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_task.id)
        assert data["title"] == test_task.title
        assert data["owner_id"] == str(test_user.id)

    @pytest.mark.asyncio
    async def test_get_task_success_as_assignee(
        self, client: AsyncClient, test_user, test_task
    ):
        """Test retrieving a task as the assigned user"""
        # Create another user and assign task to them
        user2_response = await client.post(
            "/api/users",
            json={
                "name": "User Two",
                "email": "user2@example.com",
                "password": "pass123",
            },
        )
        user2_id = user2_response.json()["id"]

        # Update task to assign to user2
        await client.put(
            f"/api/tasks/{test_task.id}",
            json={"assigned_to_id": user2_id},
            params={"user_id": str(test_user.id)},
        )

        # Get task as assignee
        response = await client.get(
            f"/api/tasks/{test_task.id}",
            params={"user_id": user2_id},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["assigned_to_id"] == user2_id

    @pytest.mark.asyncio
    async def test_get_task_not_found(self, client: AsyncClient, test_user):
        """Test retrieving a non-existent task"""
        fake_id = uuid4()
        response = await client.get(
            f"/api/tasks/{fake_id}",
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_get_task_permission_denied(self, client: AsyncClient, test_task):
        """Test unauthorized user cannot access task"""
        # Create a different user
        user_response = await client.post(
            "/api/users",
            json={
                "name": "Other User",
                "email": "other@example.com",
                "password": "pass123",
            },
        )
        other_user_id = user_response.json()["id"]

        response = await client.get(
            f"/api/tasks/{test_task.id}",
            params={"user_id": other_user_id},
        )

        assert response.status_code == 403
        assert "permission" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_get_task_invalid_uuid(self, client: AsyncClient, test_user):
        """Test retrieving task with invalid UUID format"""
        response = await client.get(
            "/api/tasks/not-a-uuid",
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 422


class TestListUserTasks:
    """Test suite for list user tasks endpoint"""

    @pytest.mark.asyncio
    async def test_list_user_tasks_success(
        self, client: AsyncClient, test_user, test_task
    ):
        """Test listing user's own tasks"""
        response = await client.get(
            "/api/tasks",
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(task["id"] == str(test_task.id) for task in data)

    @pytest.mark.asyncio
    async def test_list_user_tasks_empty(self, client: AsyncClient):
        """Test listing tasks for user with no tasks"""
        # Create a user with no tasks
        user_response = await client.post(
            "/api/users",
            json={
                "name": "Empty User",
                "email": "empty@example.com",
                "password": "pass123",
            },
        )
        user_id = user_response.json()["id"]

        response = await client.get(
            "/api/tasks",
            params={"user_id": user_id},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_list_user_tasks_with_status_filter(
        self, client: AsyncClient, test_user, test_task
    ):
        """Test listing user's tasks filtered by status"""
        # Create multiple tasks with different statuses
        await client.post(
            "/api/tasks",
            json={"title": "In progress task"},
            params={"owner_id": str(test_user.id)},
        )

        response = await client.get(
            "/api/tasks",
            params={"user_id": str(test_user.id), "status": "pending"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(task["status"] == "pending" for task in data)

    @pytest.mark.asyncio
    async def test_list_user_tasks_filter_no_results(
        self, client: AsyncClient, test_user
    ):
        """Test list with status filter that has no results"""
        response = await client.get(
            "/api/tasks",
            params={"user_id": str(test_user.id), "status": "completed"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0


class TestListAssignedTasks:
    """Test suite for list assigned tasks endpoint"""

    @pytest.mark.asyncio
    async def test_list_assigned_tasks_success(self, client: AsyncClient, test_user):
        """Test listing tasks assigned to user"""
        # Create a task assigned to test_user
        await client.post(
            "/api/tasks",
            json={
                "title": "Assigned task",
                "assigned_to_id": str(test_user.id),
            },
            params={"owner_id": str(uuid4())},
        )

        response = await client.get(
            "/api/tasks/assigned",
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_list_assigned_tasks_empty(self, client: AsyncClient):
        """Test listing assigned tasks for user with none"""
        user_response = await client.post(
            "/api/users",
            json={
                "name": "No Assigned User",
                "email": "noassigned@example.com",
                "password": "pass123",
            },
        )
        user_id = user_response.json()["id"]

        response = await client.get(
            "/api/tasks/assigned",
            params={"user_id": user_id},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0


class TestUpdateTask:
    """Test suite for update task endpoint"""

    @pytest.mark.asyncio
    async def test_update_task_title(self, client: AsyncClient, test_user, test_task):
        """Test updating task title"""
        response = await client.put(
            f"/api/tasks/{test_task.id}",
            json={"title": "Updated Title"},
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == test_task.description

    @pytest.mark.asyncio
    async def test_update_task_status(self, client: AsyncClient, test_user, test_task):
        """Test updating task status"""
        response = await client.put(
            f"/api/tasks/{test_task.id}",
            json={"status": "in_progress"},
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "in_progress"

    @pytest.mark.asyncio
    async def test_update_task_multiple_fields(
        self, client: AsyncClient, test_user, test_task
    ):
        """Test updating multiple fields"""
        new_due_date = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()

        response = await client.put(
            f"/api/tasks/{test_task.id}",
            json={
                "title": "New Title",
                "status": "completed",
                "description": "Updated description",
                "due_date": new_due_date,
            },
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["status"] == "completed"
        assert data["description"] == "Updated description"

    @pytest.mark.asyncio
    async def test_update_task_assign_to_user(
        self, client: AsyncClient, test_user, test_task
    ):
        """Test assigning task to another user"""
        user2_response = await client.post(
            "/api/users",
            json={
                "name": "Assignee User",
                "email": "assignee@example.com",
                "password": "pass123",
            },
        )
        user2_id = user2_response.json()["id"]

        response = await client.put(
            f"/api/tasks/{test_task.id}",
            json={"assigned_to_id": user2_id},
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["assigned_to_id"] == user2_id

    @pytest.mark.asyncio
    async def test_update_task_not_found(self, client: AsyncClient, test_user):
        """Test updating non-existent task"""
        fake_id = uuid4()
        response = await client.put(
            f"/api/tasks/{fake_id}",
            json={"title": "Updated"},
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_task_permission_denied(self, client: AsyncClient, test_task):
        """Test non-owner cannot update task"""
        user_response = await client.post(
            "/api/users",
            json={
                "name": "Other User",
                "email": "other@example.com",
                "password": "pass123",
            },
        )
        other_user_id = user_response.json()["id"]

        response = await client.put(
            f"/api/tasks/{test_task.id}",
            json={"title": "Hacked Title"},
            params={"user_id": other_user_id},
        )

        assert response.status_code == 403
        assert "owner" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_update_task_partial(self, client: AsyncClient, test_user, test_task):
        """Test that only provided fields are updated"""
        original_description = test_task.description

        response = await client.put(
            f"/api/tasks/{test_task.id}",
            json={"title": "Only Title Changed"},
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Only Title Changed"
        assert data["description"] == original_description


class TestDeleteTask:
    """Test suite for delete task endpoint"""

    @pytest.mark.asyncio
    async def test_delete_task_success(self, client: AsyncClient, test_user, test_task):
        """Test successful task deletion by owner"""
        response = await client.delete(
            f"/api/tasks/{test_task.id}",
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 204

        # Verify task is actually deleted
        get_response = await client.get(
            f"/api/tasks/{test_task.id}",
            params={"user_id": str(test_user.id)},
        )
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, client: AsyncClient, test_user):
        """Test deleting non-existent task"""
        fake_id = uuid4()
        response = await client.delete(
            f"/api/tasks/{fake_id}",
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_task_permission_denied(self, client: AsyncClient, test_task):
        """Test non-owner cannot delete task"""
        user_response = await client.post(
            "/api/users",
            json={
                "name": "Other User",
                "email": "other@example.com",
                "password": "pass123",
            },
        )
        other_user_id = user_response.json()["id"]

        response = await client.delete(
            f"/api/tasks/{test_task.id}",
            params={"user_id": other_user_id},
        )

        assert response.status_code == 403
        assert "owner" in response.json()["detail"].lower()


class TestTaskStatusValidation:
    """Test suite for task status enum validation"""

    @pytest.mark.asyncio
    async def test_valid_status_values(self, client: AsyncClient, test_user, test_task):
        """Test all valid status values"""
        valid_statuses = ["pending", "in_progress", "completed"]

        for status in valid_statuses:
            response = await client.put(
                f"/api/tasks/{test_task.id}",
                json={"status": status},
                params={"user_id": str(test_user.id)},
            )
            assert response.status_code == 200
            assert response.json()["status"] == status

    @pytest.mark.asyncio
    async def test_invalid_status_value(
        self, client: AsyncClient, test_user, test_task
    ):
        """Test invalid status value is rejected"""
        response = await client.put(
            f"/api/tasks/{test_task.id}",
            json={"status": "invalid_status"},
            params={"user_id": str(test_user.id)},
        )

        assert response.status_code == 422
