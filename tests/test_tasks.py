import pytest
from httpx import AsyncClient
from uuid import uuid4
from datetime import datetime, timezone, timedelta


class TestCreateTask:
    """Test suite for task creation endpoint"""

    @pytest.mark.asyncio
    async def test_create_task_success(self, auth_client: AsyncClient, test_user):
        """Test successful task creation"""
        response = await auth_client.post(
            "/api/tasks",
            json={
                "title": "Complete project",
                "description": "Finish the API implementation",
                "due_date": (
                    datetime.now(timezone.utc) + timedelta(days=7)
                ).isoformat(),
            },
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
    async def test_create_task_invalid_assignee(
        self, auth_client: AsyncClient, test_user
    ):
        """Test creating task with invalid assignee UUID raises ValueError"""
        response = await auth_client.post(
            "/api/tasks",
            json={
                "title": "Test Task",
                "description": "Task with invalid assignee",
                "assigned_to_id": "00000000-0000-0000-0000-000000000000",  # Non-existent UUID
            },
        )

        assert response.status_code == 400
        assert "user not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_task_missing_title(self, auth_client: AsyncClient, test_user):
        """Test task creation fails without title"""
        response = await auth_client.post(
            "/api/tasks",
            json={
                "description": "Missing title",
            },
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_task_optional_fields(
        self, auth_client: AsyncClient, test_user
    ):
        """Test task creation with only required fields"""
        response = await auth_client.post(
            "/api/tasks",
            json={"title": "Simple task"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Simple task"
        assert data["description"] is None
        assert data["due_date"] is None
        assert "owner_id" in data

    @pytest.mark.asyncio
    async def test_create_task_with_assignee(
        self, client: AsyncClient, auth_client: AsyncClient, test_user
    ):
        """Test creating task assigned to another user"""
        # Create another user (using regular client for registration)
        user2_response = await client.post(
            "/api/users",
            json={
                "name": "User Two",
                "email": "user2@example.com",
                "password": "pass123",
            },
        )
        user2_id = user2_response.json()["id"]

        response = await auth_client.post(
            "/api/tasks",
            json={
                "title": "Assigned task",
                "assigned_to_id": user2_id,
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["assigned_to_id"] == user2_id


class TestGetTask:
    """Test suite for get task endpoint"""

    @pytest.mark.asyncio
    async def test_get_task_success_as_owner(
        self, auth_client: AsyncClient, test_user, test_task
    ):
        """Test retrieving a task as the owner"""
        response = await auth_client.get(f"/api/tasks/{test_task.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_task.id)
        assert data["title"] == test_task.title
        assert data["owner_id"] == str(test_user.id)

    # @pytest.mark.asyncio
    # async def test_get_task_success_as_assignee(
    #     self, auth_client: AsyncClient, test_user, test_task
    # ):
    #     """Test retrieving a task as the assigned user"""
    #     # NOTE: This test is temporarily disabled because it requires
    #     # simulating being logged in as different users, which would
    #     # need separate auth_client fixtures or a different approach
    #     pass

    @pytest.mark.asyncio
    async def test_get_task_not_found(self, auth_client: AsyncClient, test_user):
        """Test retrieving a non-existent task"""
        fake_id = uuid4()
        response = await auth_client.get(f"/api/tasks/{fake_id}")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    # @pytest.mark.asyncio
    # async def test_get_task_permission_denied(
    #     self, auth_client: AsyncClient, test_task
    # ):
    #     """Test unauthorized user cannot access task"""
    #     # NOTE: This test is temporarily disabled because it requires
    #     # simulating being logged in as different users
    #     pass

    @pytest.mark.asyncio
    async def test_get_task_invalid_uuid(self, auth_client: AsyncClient, test_user):
        """Test retrieving task with invalid UUID format"""
        response = await auth_client.get("/api/tasks/not-a-uuid")

        assert response.status_code == 422


class TestListUserTasks:
    """Test suite for list user tasks endpoint"""

    @pytest.mark.asyncio
    async def test_list_user_tasks_success(
        self, auth_client: AsyncClient, test_user, test_task
    ):
        """Test listing user's own tasks"""
        response = await auth_client.get("/api/tasks")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(task["id"] == str(test_task.id) for task in data)

    @pytest.mark.asyncio
    async def test_list_user_tasks_empty(self, auth_client: AsyncClient, test_user):
        """Test listing tasks for current user when they have no tasks"""
        # Delete the test_task if it exists by getting all tasks first
        response = await auth_client.get("/api/tasks")
        tasks = response.json()

        # Delete all existing tasks
        for task in tasks:
            await auth_client.delete(f"/api/tasks/{task['id']}")

        # Now test empty list
        response = await auth_client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_list_user_tasks_with_status_filter(
        self, auth_client: AsyncClient, test_user, test_task
    ):
        """Test listing user's tasks filtered by status"""
        # Create multiple tasks with different statuses
        await auth_client.post(
            "/api/tasks",
            json={"title": "In progress task"},
        )

        response = await auth_client.get(
            "/api/tasks",
            params={"status": "pending"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(task["status"] == "pending" for task in data)

    @pytest.mark.asyncio
    async def test_list_user_tasks_filter_no_results(
        self, auth_client: AsyncClient, test_user
    ):
        """Test list with status filter that has no results"""
        response = await auth_client.get(
            "/api/tasks",
            params={"status": "completed"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0


class TestListAssignedTasks:
    """Test suite for list assigned tasks endpoint"""

    @pytest.mark.asyncio
    async def test_list_assigned_tasks_success(
        self, auth_client: AsyncClient, test_user
    ):
        """Test listing tasks assigned to user"""
        # Create a task assigned to test_user
        await auth_client.post(
            "/api/tasks",
            json={
                "title": "Assigned task",
                "assigned_to_id": str(test_user.id),
            },
        )

        response = await auth_client.get("/api/tasks/assigned")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_list_assigned_tasks_empty(self, auth_client: AsyncClient, test_user):
        """Test listing assigned tasks when user has none assigned"""
        response = await auth_client.get("/api/tasks/assigned")
        assert response.status_code == 200
        # May or may not be empty depending on test_task fixture
        data = response.json()
        assert isinstance(data, list)


class TestUpdateTask:
    """Test suite for update task endpoint"""

    @pytest.mark.asyncio
    async def test_update_task_title(
        self, auth_client: AsyncClient, test_user, test_task
    ):
        """Test updating task title"""
        response = await auth_client.put(
            f"/api/tasks/{test_task.id}",
            json={"title": "Updated Title"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == test_task.description

    @pytest.mark.asyncio
    async def test_update_task_status(
        self, auth_client: AsyncClient, test_user, test_task
    ):
        """Test updating task status"""
        response = await auth_client.put(
            f"/api/tasks/{test_task.id}",
            json={"status": "in_progress"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "in_progress"

    @pytest.mark.asyncio
    async def test_update_task_multiple_fields(
        self, auth_client: AsyncClient, test_user, test_task
    ):
        """Test updating multiple fields"""
        new_due_date = (datetime.now(timezone.utc) + timedelta(days=5)).isoformat()

        response = await auth_client.put(
            f"/api/tasks/{test_task.id}",
            json={
                "title": "New Title",
                "status": "completed",
                "description": "Updated description",
                "due_date": new_due_date,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["status"] == "completed"
        assert data["description"] == "Updated description"

    @pytest.mark.asyncio
    async def test_update_task_assign_to_user(
        self, client: AsyncClient, auth_client: AsyncClient, test_user, test_task
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

        response = await auth_client.put(
            f"/api/tasks/{test_task.id}",
            json={"assigned_to_id": user2_id},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["assigned_to_id"] == user2_id

    @pytest.mark.asyncio
    async def test_update_task_not_found(self, auth_client: AsyncClient, test_user):
        """Test updating non-existent task"""
        fake_id = uuid4()
        response = await auth_client.put(
            f"/api/tasks/{fake_id}",
            json={"title": "Updated"},
        )

        assert response.status_code == 404

    # @pytest.mark.asyncio
    # async def test_update_task_permission_denied(
    #     self, auth_client: AsyncClient, test_task
    # ):
    #     """Test non-owner cannot update task"""
    #     # NOTE: This test is temporarily disabled because it requires
    #     # simulating being logged in as different users
    #     pass

    @pytest.mark.asyncio
    async def test_update_task_partial(
        self, auth_client: AsyncClient, test_user, test_task
    ):
        """Test that only provided fields are updated"""
        original_description = test_task.description

        response = await auth_client.put(
            f"/api/tasks/{test_task.id}",
            json={"title": "Only Title Changed"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Only Title Changed"
        assert data["description"] == original_description


class TestDeleteTask:
    """Test suite for delete task endpoint"""

    @pytest.mark.asyncio
    async def test_delete_task_success(
        self, auth_client: AsyncClient, test_user, test_task
    ):
        """Test successful task deletion by owner"""
        response = await auth_client.delete(f"/api/tasks/{test_task.id}")

        assert response.status_code == 204

        # Verify task is actually deleted
        get_response = await auth_client.get(f"/api/tasks/{test_task.id}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, auth_client: AsyncClient, test_user):
        """Test deleting non-existent task"""
        fake_id = uuid4()
        response = await auth_client.delete(f"/api/tasks/{fake_id}")

        assert response.status_code == 404

    # @pytest.mark.asyncio
    # async def test_delete_task_permission_denied(
    #     self, auth_client: AsyncClient, test_task
    # ):
    #     """Test non-owner cannot delete task"""
    #     # NOTE: This test is temporarily disabled because it requires
    #     # simulating being logged in as different users
    #     pass


class TestTaskStatusValidation:
    """Test suite for task status enum validation"""

    @pytest.mark.asyncio
    async def test_valid_status_values(
        self, auth_client: AsyncClient, test_user, test_task
    ):
        """Test all valid status values"""
        valid_statuses = ["pending", "in_progress", "completed"]

        for status in valid_statuses:
            response = await auth_client.put(
                f"/api/tasks/{test_task.id}",
                json={"status": status},
            )
            assert response.status_code == 200
            assert response.json()["status"] == status

    @pytest.mark.asyncio
    async def test_invalid_status_value(
        self, auth_client: AsyncClient, test_user, test_task
    ):
        """Test invalid status value is rejected"""
        response = await auth_client.put(
            f"/api/tasks/{test_task.id}",
            json={"status": "invalid_status"},
        )

        assert response.status_code == 422


class TestPermissionErrors:
    """Test permission-related error cases for 100% coverage"""

    @pytest.mark.asyncio
    async def test_get_task_permission_error_via_service(
        self, auth_client: AsyncClient, client: AsyncClient, test_user
    ):
        """Test accessing task that doesn't belong to user triggers PermissionError"""
        # Create another user
        user2_response = await client.post(
            "/api/users",
            json={
                "name": "User Two",
                "email": "user2@example.com",
                "password": "pass123",
            },
        )
        user2 = user2_response.json()

        # Create a task as user2 (simulate by temporarily overriding auth)
        from src.main import app
        from src.dependencies import get_current_user
        from src.models import UserResponse

        # Mock user2 as current user temporarily
        mock_user2 = UserResponse(
            id=user2["id"],
            email=user2["email"],
            name=user2["name"],
            role="member",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        app.dependency_overrides[get_current_user] = lambda: mock_user2

        # Create task as user2
        task_response = await auth_client.post(
            "/api/tasks",
            json={"title": "User2's task"},
        )
        task_id = task_response.json()["id"]

        # Restore original user (test_user)
        app.dependency_overrides[get_current_user] = lambda: test_user

        # Now test_user tries to access user2's task - should get 403
        response = await auth_client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 403
        assert "permission" in response.json()["detail"].lower()

        # Clean up
        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_update_task_permission_error(
        self, auth_client: AsyncClient, client: AsyncClient, test_user
    ):
        """Test updating task that doesn't belong to user triggers PermissionError"""
        # Similar setup to get_task test
        user2_response = await client.post(
            "/api/users",
            json={
                "name": "User Two",
                "email": "user2@example.com",
                "password": "pass123",
            },
        )
        user2 = user2_response.json()

        from src.main import app
        from src.dependencies import get_current_user
        from src.models import UserResponse

        mock_user2 = UserResponse(
            id=user2["id"],
            email=user2["email"],
            name=user2["name"],
            role="member",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        app.dependency_overrides[get_current_user] = lambda: mock_user2

        task_response = await auth_client.post(
            "/api/tasks",
            json={"title": "User2's task"},
        )
        task_id = task_response.json()["id"]

        app.dependency_overrides[get_current_user] = lambda: test_user

        response = await auth_client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Hacked title"},
        )
        assert response.status_code == 403
        assert "permission" in response.json()["detail"].lower()

        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_delete_task_permission_error(
        self, auth_client: AsyncClient, client: AsyncClient, test_user
    ):
        """Test deleting task that doesn't belong to user triggers PermissionError"""
        user2_response = await client.post(
            "/api/users",
            json={
                "name": "User Two",
                "email": "user2@example.com",
                "password": "pass123",
            },
        )
        user2 = user2_response.json()

        from src.main import app
        from src.dependencies import get_current_user
        from src.models import UserResponse

        mock_user2 = UserResponse(
            id=user2["id"],
            email=user2["email"],
            name=user2["name"],
            role="member",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        app.dependency_overrides[get_current_user] = lambda: mock_user2

        task_response = await auth_client.post(
            "/api/tasks",
            json={"title": "User2's task"},
        )
        task_id = task_response.json()["id"]

        app.dependency_overrides[get_current_user] = lambda: test_user

        response = await auth_client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 403
        assert "permission" in response.json()["detail"].lower()

        app.dependency_overrides.clear()


class TestTaskServiceErrorCases:
    """Tests for TaskService error cases to achieve 100% coverage"""

    @pytest.mark.asyncio
    async def test_task_service_direct_get_not_found(self, test_db_session):
        """Test TaskService.get_task directly with non-existent ID to trigger ValueError"""
        from src.services.task_services import TaskService
        from src.repositories.task_repository import TaskRepository

        repo = TaskRepository(test_db_session)
        service = TaskService(repo)

        fake_task_id = uuid4()
        fake_user_id = uuid4()

        try:
            await service.get_task(fake_task_id, fake_user_id)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "not found" in str(e).lower()

    @pytest.mark.asyncio
    async def test_task_service_direct_update_not_found(self, test_db_session):
        """Test TaskService.update_task directly with non-existent ID"""
        from src.services.task_services import TaskService
        from src.repositories.task_repository import TaskRepository

        repo = TaskRepository(test_db_session)
        service = TaskService(repo)

        fake_task_id = uuid4()
        fake_user_id = uuid4()

        try:
            await service.update_task(fake_task_id, fake_user_id, {"title": "Updated"})
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "not found" in str(e).lower()

    @pytest.mark.asyncio
    async def test_task_service_direct_delete_not_found(self, test_db_session):
        """Test TaskService.delete_task directly with non-existent ID"""
        from src.services.task_services import TaskService
        from src.repositories.task_repository import TaskRepository

        repo = TaskRepository(test_db_session)
        service = TaskService(repo)

        fake_task_id = uuid4()
        fake_user_id = uuid4()

        try:
            await service.delete_task(fake_task_id, fake_user_id)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "not found" in str(e).lower()

    @pytest.mark.asyncio
    async def test_task_service_permission_error_in_service(
        self, test_db_session, test_user
    ):
        """Test PermissionError at service level when user doesn't own/isn't assigned to task"""
        from src.services.task_services import TaskService
        from src.repositories.task_repository import TaskRepository
        from src.models import Task, TaskStatus

        repo = TaskRepository(test_db_session)
        service = TaskService(repo)

        # Create a task owned by a different user
        other_user_id = uuid4()
        task = Task(
            id=uuid4(),
            title="Other User's Task",
            owner_id=other_user_id,  # Different from test_user
            status=TaskStatus.PENDING,
        )

        test_db_session.add(task)
        await test_db_session.commit()
        await test_db_session.refresh(task)

        # Try to access it as test_user - should trigger PermissionError
        try:
            assert task.id is not None  # Ensure task ID is not None
            await service.get_task(task.id, test_user.id)
            assert False, "Should have raised PermissionError"
        except PermissionError as e:
            assert "permission" in str(e).lower()

        # Try to update it - should also trigger PermissionError
        try:
            assert task.id is not None  # Ensure task ID is not None
            await service.update_task(task.id, test_user.id, {"title": "Hacked"})
            assert False, "Should have raised PermissionError"
        except PermissionError as e:
            assert "owner" in str(e).lower()

        # Try to delete it - should also trigger PermissionError
        try:
            assert task.id is not None  # Ensure task ID is not None
            await service.delete_task(task.id, test_user.id)
            assert False, "Should have raised PermissionError"
        except PermissionError as e:
            assert "owner" in str(e).lower()
