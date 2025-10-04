import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client() -> APIClient:
    """Фикстура для проверки HTTP-запросов."""

    return APIClient()


@pytest.fixture
def user_api_client(api_client: APIClient, user: User) -> APIClient:
    """Фикстура пользователя для проверки HHTP-запросов с ролью user."""

    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user() -> User:
    """Фикстура пользователя."""

    return User.objects.create(email="user1@mail.ru")


@pytest.fixture
def admin() -> User:
    """Фикстура администратора(роль - admin)."""

    return User.objects.create(email="admin@mail.ru", role="admin")
