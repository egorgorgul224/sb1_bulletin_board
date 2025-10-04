import pytest
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
def test_create_user(api_client: APIClient) -> None:
    """Тест проверяет создание пользователя."""

    payload = {"email": "admin@mail.ru", "password": "12345"}
    response = api_client.post(reverse("users:register"), data=payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == payload["email"]
    assert User.objects.count() == 1
    assert User.objects.filter(email="admin@mail.ru").exists()


@pytest.mark.django_db
def test_str_user(user: User) -> None:
    """Тест проверяет корректный вывод str-строки модели User."""

    assert str(user) == f"{user.email}, {user.is_active}"


@pytest.mark.django_db
def test_create_superuser(capsys: pytest.CaptureFixture) -> None:
    """Тест проверяет создание суперпользователя командой createadmin."""

    assert not User.objects.exists()
    call_command("createadmin")
    superuser = User.objects.first()
    assert superuser.is_superuser
    assert superuser.is_staff
    assert superuser.check_password("12345")
    assert User.objects.count() == 1

    captured = capsys.readouterr()
    assert "Successfully created admin user with email admin@mail.ru" in captured.out


@pytest.mark.django_db
def test_create_superuser_exists(capsys: pytest.CaptureFixture, admin: User) -> None:
    """Тест проверяет повторное создание суперпользователя командой createadmin и вывод сообщения."""

    call_command("createadmin")

    captured = capsys.readouterr()
    assert "Superuser with this email already exists." in captured.out


@pytest.mark.django_db
def test_user_list(user_api_client: APIClient, user: User) -> None:
    """Тест проверяет вывод списка пользователей"""

    response = user_api_client.get(reverse("users:user_list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_user_detail(user_api_client: APIClient, user: User) -> None:
    """Тест проверяет просмотр информации о пользователе."""

    response = user_api_client.get(reverse("users:user_detail", kwargs={"pk": user.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email
    assert response.data["first_name"] == ""
    assert response.data["last_name"] == ""


@pytest.mark.django_db
def test_user_update(user_api_client: APIClient, user: User) -> None:
    """Тест проверяет обновление данных пользователя."""

    payload = {
        "first_name": "Ivan",
        "last_name": "Ivanov",
    }
    response = user_api_client.patch(reverse("users:user_update", kwargs={"pk": user.pk}), data=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == payload["first_name"]
    assert response.data["last_name"] == payload["last_name"]


@pytest.mark.django_db
def test_user_update_wo_access(user_api_client: APIClient, user: User) -> None:
    """Тест проверяет корректную обработку изменения данных пользователя без права доступа."""

    user_second = User.objects.create(email="user2@mail.ru")
    payload = {"first_name": "Name"}
    response = user_api_client.patch(reverse("users:user_update", kwargs={"pk": user_second.pk}), data=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_delete(user_api_client: APIClient, user: User) -> None:
    """Тестирование удаления пользователя."""

    response = user_api_client.delete(reverse("users:user_delete", kwargs={"pk": user.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_user_delete_wo_access(user_api_client: APIClient, user: User) -> None:
    """Тест проверяет корректную обработку удаления пользователя без права доступа."""

    user_second = User.objects.create(email="user2@mail.ru")
    response = user_api_client.delete(reverse("users:user_delete", kwargs={"pk": user_second.pk}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert User.objects.count() == 2
