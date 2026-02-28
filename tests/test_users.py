import pytest
from httpx import AsyncClient
from uuid import uuid4


class TestUserRegistration:
    """Test suite for user registration endpoint"""

    @pytest.mark.asyncio
    async def test_register_user_success(self, client: AsyncClient):
        """Test successful user registration"""
        response = await client.post(
            "/api/users",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "password": "securepass123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "john@example.com"
        assert data["name"] == "John Doe"
        assert data["role"] == "member"
        assert "id" in data
        assert "password_hash" not in data  # Password should not be exposed

    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self, client: AsyncClient, test_user):
        """Test registration fails with duplicate email"""
        response = await client.post(
            "/api/users",
            json={
                "name": "Another User",
                "email": "test@example.com",  # Same as test_user
                "password": "password123",
            },
        )

        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_user_invalid_email(self, client: AsyncClient):
        """Test registration - invalid email accepted without validation"""
        response = await client.post(
            "/api/users",
            json={
                "name": "Invalid Email",
                "email": "not-an-email",
                "password": "password123",
            },
        )

        assert response.status_code == 201  # API accepts any string as email

    @pytest.mark.asyncio
    async def test_register_user_missing_fields(self, client: AsyncClient):
        """Test registration fails with missing required fields"""
        response = await client.post(
            "/api/users",
            json={
                "name": "Incomplete",
                # Missing email and password
            },
        )

        assert response.status_code == 422


class TestGetUser:
    """Test suite for get user endpoint"""

    @pytest.mark.asyncio
    async def test_get_user_success(self, client: AsyncClient, test_user):
        """Test retrieving an existing user"""
        response = await client.get(f"/api/users/{test_user.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_user.id)
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert "password_hash" not in data

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, client: AsyncClient):
        """Test retrieving a non-existent user"""
        fake_id = uuid4()
        response = await client.get(f"/api/users/{fake_id}")

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_user_invalid_uuid(self, client: AsyncClient):
        """Test retrieving user with invalid UUID format"""
        response = await client.get("/api/users/not-a-uuid")

        assert response.status_code == 422


class TestUpdateUser:
    """Test suite for update user endpoint"""

    @pytest.mark.asyncio
    async def test_update_user_name(self, client: AsyncClient, test_user):
        """Test updating user name"""
        response = await client.put(
            f"/api/users/{test_user.id}",
            json={"name": "Updated Name"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["email"] == "test@example.com"  # Email unchanged

    @pytest.mark.asyncio
    async def test_update_user_email(self, client: AsyncClient, test_user):
        """Test updating user email"""
        response = await client.put(
            f"/api/users/{test_user.id}",
            json={"email": "newemail@example.com"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newemail@example.com"

    @pytest.mark.asyncio
    async def test_update_user_password(self, client: AsyncClient, test_user):
        """Test updating user password"""
        response = await client.put(
            f"/api/users/{test_user.id}",
            json={"password": "newpassword123"},
        )

        assert response.status_code == 200
        data = response.json()
        # Verify password was hashed (field shouldn't be exposed)
        assert "password_hash" not in data
        assert "password" not in data

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, client: AsyncClient):
        """Test updating a non-existent user"""
        fake_id = uuid4()
        response = await client.put(
            f"/api/users/{fake_id}",
            json={"name": "New Name"},
        )

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_update_user_duplicate_email(self, client: AsyncClient, test_user):
        """Test updating user email to an existing email fails"""
        # Create a second user
        user2_response = await client.post(
            "/api/users",
            json={
                "name": "User Two",
                "email": "user2@example.com",
                "password": "pass123",
            },
        )
        user2_id = user2_response.json()["id"]

        # Try to update user2 with test_user's email
        response = await client.put(
            f"/api/users/{user2_id}",
            json={"email": "test@example.com"},
        )

        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_update_user_partial_update(self, client: AsyncClient, test_user):
        """Test that only provided fields are updated"""
        original_email = test_user.email

        response = await client.put(
            f"/api/users/{test_user.id}",
            json={"name": "Only Name Updated"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Only Name Updated"
        assert data["email"] == original_email  # Should remain unchanged

    @pytest.mark.asyncio
    async def test_update_user_multiple_fields(self, client: AsyncClient, test_user):
        """Test updating multiple fields at once"""
        response = await client.put(
            f"/api/users/{test_user.id}",
            json={
                "name": "New Name",
                "email": "newemail@example.com",
                "password": "newpass456",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Name"
        assert data["email"] == "newemail@example.com"


class TestHealthCheck:
    """Test suite for health check endpoint"""

    @pytest.mark.asyncio
    async def test_health_check_success(self, client: AsyncClient):
        """Test health check endpoint returns healthy status"""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data
