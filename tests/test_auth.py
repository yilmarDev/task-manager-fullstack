import pytest
from httpx import AsyncClient
import jwt
from src.config import settings


class TestLogin:
    """Test suite for authentication login endpoint"""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login with valid credentials"""
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",  # OAuth2PasswordRequestForm uses 'username' field
                "password": "testpass123",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

        # Verify the token is valid JWT and contains correct user info
        token = data["access_token"]
        decoded = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        assert decoded["sub"] == str(test_user.id)
        assert "exp" in decoded  # Token should have expiration

    @pytest.mark.asyncio
    async def test_login_invalid_email(self, client: AsyncClient, test_user):
        """Test login with non-existent email"""
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "nonexistent@example.com",
                "password": "testpass123",
            },
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
        assert response.headers.get("WWW-Authenticate") == "Bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client: AsyncClient, test_user):
        """Test login with incorrect password"""
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "wrongpassword",
            },
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
        assert response.headers.get("WWW-Authenticate") == "Bearer"

    @pytest.mark.asyncio
    async def test_login_missing_credentials(self, client: AsyncClient):
        """Test login with missing credentials"""
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                # Missing password
            },
        )

        assert response.status_code == 422  # ValidationError from FastAPI

    @pytest.mark.asyncio
    async def test_login_empty_credentials(self, client: AsyncClient):
        """Test login with empty credentials"""
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "",
                "password": "",
            },
        )

        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_wrong_content_type(self, client: AsyncClient, test_user):
        """Test login with JSON instead of form data (should fail)"""
        response = await client.post(
            "/api/auth/login",
            json={  # OAuth2PasswordRequestForm expects form data, not JSON
                "username": "test@example.com",
                "password": "testpass123",
            },
        )

        assert response.status_code == 422  # ValidationError


class TestTokenValidation:
    """Test suite for validating JWT tokens work with protected endpoints"""

    @pytest.mark.asyncio
    async def test_authenticated_request_with_valid_token(
        self, client: AsyncClient, test_user
    ):
        """Test that a valid token allows access to protected endpoints"""
        # First, login to get a token
        login_response = await client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123",
            },
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Use the token to access a protected endpoint
        response = await client.get(
            f"/api/users/{test_user.id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_user.id)

    @pytest.mark.asyncio
    async def test_authenticated_request_with_invalid_token(
        self, client: AsyncClient, test_user
    ):
        """Test that an invalid token is rejected"""
        response = await client.get(
            f"/api/users/{test_user.id}",
            headers={"Authorization": "Bearer invalid_token_here"},
        )

        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_authenticated_request_with_malformed_header(
        self, client: AsyncClient, test_user
    ):
        """Test that malformed Authorization header is rejected"""
        response = await client.get(
            f"/api/users/{test_user.id}",
            headers={"Authorization": "InvalidFormat token_here"},
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_authenticated_request_without_token(
        self, client: AsyncClient, test_user
    ):
        """Test that protected endpoints require authentication"""
        response = await client.get(f"/api/users/{test_user.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_token_with_expired_signature(self, client: AsyncClient, test_user):
        """Test that tokens with tampered signature are rejected"""
        # Get a valid token
        login_response = await client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123",
            },
        )
        token = login_response.json()["access_token"]

        # Tamper with the token (change last character)
        tampered_token = token[:-1] + ("a" if token[-1] != "a" else "b")

        response = await client.get(
            f"/api/users/{test_user.id}",
            headers={"Authorization": f"Bearer {tampered_token}"},
        )

        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]


class TestTokenContent:
    """Test suite for JWT token content validation"""

    @pytest.mark.asyncio
    async def test_token_contains_correct_user_id(self, client: AsyncClient, test_user):
        """Test that the JWT token contains the correct user ID"""
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123",
            },
        )

        token = response.json()["access_token"]
        decoded = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )

        assert decoded["sub"] == str(test_user.id)

    @pytest.mark.asyncio
    async def test_token_has_expiration_time(self, client: AsyncClient, test_user):
        """Test that tokens have an expiration time"""
        response = await client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123",
            },
        )

        token = response.json()["access_token"]
        decoded = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )

        assert "exp" in decoded
        assert decoded["exp"] > 0  # Should be a valid timestamp

    @pytest.mark.asyncio
    async def test_multiple_logins_generate_different_tokens(
        self, client: AsyncClient, test_user
    ):
        """Test that multiple logins generate different tokens (due to different exp times)"""
        # First login
        response1 = await client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123",
            },
        )
        token1 = response1.json()["access_token"]

        # Second login (small delay for different timestamp)
        import asyncio

        await asyncio.sleep(0.1)

        response2 = await client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123",
            },
        )
        token2 = response2.json()["access_token"]

        # Tokens should be different due to different expiration times
        assert token1 != token2

        # Both tokens should be valid for the same user
        decoded1 = jwt.decode(
            token1, settings.secret_key, algorithms=[settings.algorithm]
        )
        decoded2 = jwt.decode(
            token2, settings.secret_key, algorithms=[settings.algorithm]
        )
        assert decoded1["sub"] == decoded2["sub"] == str(test_user.id)
