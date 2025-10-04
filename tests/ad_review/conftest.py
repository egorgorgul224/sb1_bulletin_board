import pytest
from rest_framework.test import APIClient

from ads.models import Ad, Review
from users.models import User


@pytest.fixture
def api_client() -> APIClient:
    """Фикстура для проверки HTTP-запросов."""

    return APIClient()


@pytest.fixture
def user_api_client(api_client: APIClient, user_first: User) -> APIClient:
    """Фикстура пользователя для проверки HHTP-запросов с ролью user."""

    api_client.force_authenticate(user=user_first)
    return api_client


@pytest.fixture
def admin_api_client(api_client: APIClient, admin: User) -> APIClient:
    """Фикстура пользователя для проверки HHTP-запросов с ролью admin."""

    api_client.force_authenticate(user=admin)
    return api_client


@pytest.fixture
def user_first() -> User:
    """Фикстура пользователя для проверки отзывов."""

    return User.objects.create(email="user1@mail.ru")


@pytest.fixture
def user_second() -> User:
    """Фикстура пользователя для проверки отзывов."""

    return User.objects.create(email="user2@mail.ru")


@pytest.fixture
def admin() -> User:
    """Фикстура пользователя(роль - admin) для проверки отзывов."""

    return User.objects.create(email="admin@mail.ru", role="admin")


@pytest.fixture
def ad_first(user_first: User) -> Ad:
    """Фикстура создания объявления."""

    return Ad.objects.create(
        title="Объявление 1",
        price=1000,
        description="Тестовое объявление",
        author=user_first,
    )


@pytest.fixture
def ad_second(user_second: User) -> Ad:
    """Фикстура создания объявления."""

    return Ad.objects.create(
        title="Объявление 2",
        price=2000,
        description="Другое объявление",
        author=user_second,
    )


@pytest.fixture
def review_first(user_first: User, ad_first: Ad) -> Review:
    """Фикстура создания отзыва."""

    return Review.objects.create(text="Отзыв 1", author=user_first, ad=ad_first)


@pytest.fixture
def review_second(user_second: User, ad_second: Ad) -> Review:
    """Фикстура создания отзыва."""

    return Review.objects.create(text="Отзыв 2", author=user_second, ad=ad_second)
