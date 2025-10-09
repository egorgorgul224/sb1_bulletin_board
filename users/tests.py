import secrets
from unittest.mock import MagicMock, patch

import pytest
from django.core.management import call_command
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from jwt.utils import force_bytes
from rest_framework import status
from rest_framework.test import APIClient

from config import settings
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
    assert len(response.data) == 2


@pytest.mark.django_db
def test_user_detail(user_api_client: APIClient, user_first: User) -> None:
    """Тест проверяет просмотр информации о пользователе."""

    response = user_api_client.get(reverse("users:user_detail", kwargs={"pk": user_first.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user_first.email
    assert response.data["first_name"] == ""
    assert response.data["last_name"] == ""


@pytest.mark.django_db
def test_user_update(user_api_client: APIClient, user_first: User) -> None:
    """Тест проверяет обновление данных пользователя."""

    payload = {
        "first_name": "Ivan",
        "last_name": "Ivanov",
    }
    response = user_api_client.patch(reverse("users:user_update", kwargs={"pk": user_first.pk}), data=payload)
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
def test_user_delete(user_api_client: APIClient, user_first: User) -> None:
    """Тестирование удаления пользователя."""

    response = user_api_client.delete(reverse("users:user_delete", kwargs={"pk": user_first.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_user_delete_wo_access(user_api_client: APIClient, user: User) -> None:
    """Тест проверяет корректную обработку удаления пользователя без права доступа."""

    user_second = User.objects.create(email="user2@mail.ru")
    response = user_api_client.delete(reverse("users:user_delete", kwargs={"pk": user_second.pk}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert User.objects.count() == 3


@pytest.mark.django_db
def test_reset_password(api_client: APIClient, user: User) -> None:
    """Тест проверяет корректную обработку запроса на сброс пароля."""

    data = {"email": user.email}
    response = api_client.post(reverse("users:reset_password"), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"detail": "Ссылка для сброса пароля отправлена."}


@pytest.mark.django_db
def test_reset_password_wo_email(api_client: APIClient) -> None:
    """Тест проверяет корректную обработку запроса на сброс пароля, когда email пользователя не был найден."""

    data = {"email": "test@mail.ru"}
    response = api_client.post(reverse("users:reset_password"), data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"detail": "Пользователь с данным email не найден."}


@pytest.mark.django_db
@patch("users.services.send_password_reset_email")
def test_send_password_reset_email(mock_send_password_reset_email: MagicMock, user: User) -> None:
    """Тест проверяет корректную отправку сообщения со ссылкой на сброс пароля."""

    subject = "Тема письма"
    message = "Сообщение"
    email = [user.email]
    mock_send_password_reset_email(subject, message, settings.EMAIL_HOST_USER, email)
    assert mock_send_password_reset_email.call_count == 1
    mock_send_password_reset_email.assert_called_once_with(subject, message, settings.EMAIL_HOST_USER, email)


@pytest.mark.django_db
def test_reset_password_confirm(api_client: APIClient, user: User) -> None:
    """Тест проверяет корректное изменение пароля с помощью токена."""

    uid64 = urlsafe_base64_encode(force_bytes(str(user.pk)))
    token = secrets.token_hex(16)
    user.token = token
    user.save()
    password = "12345"

    data = {"uid": uid64, "token": token, "new_password": password}

    response = api_client.post(reverse("users:reset_password_confirm"), data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"detail": "Пароль успешно изменен."}


@pytest.mark.django_db
def test_reset_password_confirm_wo_token(api_client: APIClient, user: User) -> None:
    """Тест проверяет корректную обработку и вывод сообщения, если передан неверный токен."""

    uid64 = urlsafe_base64_encode(force_bytes(str(user.pk)))
    data = {"uid": uid64, "token": "acec19683042be9ff9f1c0c933d26bdf", "new_password": "test"}
    response = api_client.post(reverse("users:reset_password_confirm"), data=data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {"detail": "Передан неверный токен."}


@pytest.mark.django_db
def test_reset_password_confirm_wo_user(api_client: APIClient) -> None:
    """Тест проверяет корректную обработку и вывод сообщения, если пользователь не найден."""

    data = {"uid": "MQ", "token": "acec19683042be9ff9f1c0c933d26bdf", "new_password": "12345"}
    response = api_client.post(reverse("users:reset_password_confirm"), data=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"detail": "Пользователь не найден."}
