import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ads.models import Ad, Review
from users.models import User


@pytest.mark.django_db
def test_create_ad(user_api_client: APIClient, user_first: User) -> None:
    """Тест проверяет создание объявления."""

    payload = {
        "title": "Объявление 1",
        "price": 1000,
        "description": "Тестовое объявление",
    }
    response = user_api_client.post(reverse("ads:ad_create"), data=payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == payload["title"]
    assert response.data["price"] == payload["price"]
    assert response.data["description"] == payload["description"]
    assert Ad.objects.count() == 1
    ad = Ad.objects.get(title=payload["title"])
    assert ad.author == user_first


@pytest.mark.django_db
def test_str_ad(ad_first: Ad) -> None:
    """Тест проверяет корректный вывод str-строки модели Ad."""

    assert str(ad_first) == f"{ad_first.created_at}: {ad_first.title} - {ad_first.price}"


@pytest.mark.django_db
def test_list_ads(user_api_client: APIClient, ad_first: Ad, ad_second: Ad) -> None:
    """Тест проверяет вывод списка объявлений. Также проверяется корректность пагинации."""

    response = user_api_client.get(reverse("ads:ad_list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert response.data["next"] is None
    assert response.data["previous"] is None
    assert "results" in response.data
    results = response.data["results"]
    assert len(results) == 2


@pytest.mark.django_db
def test_ad_detail(user_api_client: APIClient, ad_first: Ad) -> None:
    """Тест проверяет просмотр информации об объявлении."""

    response = user_api_client.get(reverse("ads:ad_detail", kwargs={"pk": ad_first.pk}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == ad_first.pk
    assert response.data["title"] == ad_first.title
    assert response.data["price"] == ad_first.price
    assert response.data["description"] == ad_first.description


@pytest.mark.django_db
def test_ad_update(user_api_client: APIClient, ad_first: Ad) -> None:
    """Тест проверяет обновление данных объявления."""

    payload = {
        "title": "Объявление 3",
        "price": 1,
    }
    response = user_api_client.put(reverse("ads:ad_update", kwargs={"pk": ad_first.pk}), data=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == ad_first.pk
    assert response.data["title"] == payload["title"]
    assert response.data["price"] == payload["price"]


@pytest.mark.django_db
def test_ad_partial_update(user_api_client: APIClient, ad_first: Ad) -> None:
    """Тест проверяет частичное обновление данных объявления."""

    payload = {
        "title": "Объявление 4",
    }
    response = user_api_client.patch(reverse("ads:ad_update", kwargs={"pk": ad_first.pk}), data=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == ad_first.pk
    assert response.data["title"] == payload["title"]


@pytest.mark.django_db
def test_ad_update_wo_access(user_api_client: APIClient, ad_second: Ad) -> None:
    """Тест проверяет корректную обработку изменения объявление без права доступа."""

    payload = {"title": "Новое изменение"}
    response = user_api_client.patch(reverse("ads:ad_update", kwargs={"pk": ad_second.pk}), data=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_ad_delete(user_api_client: APIClient, ad_first: Ad) -> None:
    """Тестирование удаления объявления."""

    response = user_api_client.delete(reverse("ads:ad_delete", kwargs={"pk": ad_first.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ad.objects.count() == 0


@pytest.mark.django_db
def test_ad_delete_wo_access(user_api_client: APIClient, ad_second: Ad) -> None:
    """Тест проверяет корректную обработку удаления объявление без права доступа."""

    response = user_api_client.delete(reverse("ads:ad_delete", kwargs={"pk": ad_second.pk}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Ad.objects.count() == 1


@pytest.mark.django_db
def test_ad_delete_with_admin_access(admin_api_client: APIClient, ad_first: Ad) -> None:
    """Тест проверяет корректность удаления объявление администратором."""

    response = admin_api_client.delete(reverse("ads:ad_delete", kwargs={"pk": ad_first.pk}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ad.objects.count() == 0


@pytest.mark.django_db
def test_ads_list_filter(api_client: APIClient, ad_first: Ad, ad_second: Ad) -> None:
    """Тест проверяет фильтрацию объявлений по названию."""

    response = api_client.get(f"{reverse('ads:ad_list')}?title=Отзыв")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2


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
