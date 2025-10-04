import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ads.models import Ad, Review
from users.models import User


@pytest.mark.django_db
def test_create_review(user_api_client: APIClient, user_first: User, ad_first: Ad) -> None:
    """Тест проверяет создание объявления."""

    payload = {
        "text": "Отзыв",
        "ad": ad_first.pk,
    }
    response = user_api_client.post(reverse("ads:review_create"), data=payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["text"] == payload["text"]
    assert response.data["ad"] == payload["ad"]
    assert Review.objects.count() == 1
    review = Review.objects.get(text=payload["text"])
    assert review.author == user_first


@pytest.mark.django_db
def test_str_review(review_first: Review) -> None:
    """Тест проверяет корректный вывод str-строки модели Review."""

    assert str(review_first) == f"{review_first.created_at}: {review_first.ad} - {review_first.author}"


@pytest.mark.django_db
def test_list_reviews(user_api_client: APIClient, ad_first: Ad, review_first: Review) -> None:
    """Тест проверяет вывод списка отзывов."""

    response = user_api_client.get(reverse("ads:review_list", kwargs={"pk": ad_first.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_review_detail(user_api_client: APIClient, review_first: Review) -> None:
    """Тест проверяет просмотр информации отзыва."""

    response = user_api_client.get(reverse("ads:review_detail", kwargs={"pk": review_first.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == review_first.pk
    assert response.data["text"] == review_first.text
    assert response.data["ad"] == review_first.ad.id


@pytest.mark.django_db
def test_review_update(user_api_client: APIClient, review_first: Review) -> None:
    """Тест проверяет обновление данных отзыва."""

    payload = {"text": "Отзыв 10"}
    response = user_api_client.patch(reverse("ads:review_update", kwargs={"pk": review_first.pk}), data=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == review_first.pk
    assert response.data["text"] == payload["text"]


@pytest.mark.django_db
def test_review_delete(user_api_client: APIClient, review_first: Review) -> None:
    """Тестирование удаления отзыва."""

    response = user_api_client.delete(reverse("ads:review_delete", kwargs={"pk": review_first.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_review_delete_wo_access(user_api_client: APIClient, review_second: Review) -> None:
    """Тест проверяет корректную обработку удаления отзыва без права доступа."""

    response = user_api_client.delete(reverse("ads:review_delete", kwargs={"pk": review_second.pk}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_review_delete_with_admin_access(admin_api_client: APIClient, review_first: Review) -> None:
    """Тест проверяет корректность удаления отзыва администратором."""

    response = admin_api_client.delete(reverse("ads:review_delete", kwargs={"pk": review_first.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0
