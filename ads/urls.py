from django.urls import path

from ads.apps import AdsConfig
from ads.views import (AdCreateAPIView, AdDestroyAPIView, AdListAPIView, AdRetrieveAPIView, AdUpdateAPIView,
                       ReviewCreateAPIView, ReviewDestroyAPIView, ReviewListAPIView, ReviewRetrieveAPIView,
                       ReviewUpdateAPIView)

app_name = AdsConfig.name

urlpatterns = [
    # ссылки для модели Ad объявление
    path("ad/create/", AdCreateAPIView.as_view(), name="ad_create"),
    path("ads/", AdListAPIView.as_view(), name="ad_list"),
    path("ad/<int:pk>/detail/", AdRetrieveAPIView.as_view(), name="ad_detail"),
    path("ad/<int:pk>/update/", AdUpdateAPIView.as_view(), name="ad_update"),
    path("ad/<int:pk>/delete/", AdDestroyAPIView.as_view(), name="ad_delete"),
    # ссылки для модели Review отзыв
    path("review/create/", ReviewCreateAPIView.as_view(), name="review_create"),
    path("ad/<int:pk>/reviews/", ReviewListAPIView.as_view(), name="review_list"),
    path("review/<int:pk>/detail/", ReviewRetrieveAPIView.as_view(), name="review_detail"),
    path("review/<int:pk>/update/", ReviewUpdateAPIView.as_view(), name="review_update"),
    path("review/<int:pk>/delete/", ReviewDestroyAPIView.as_view(), name="review_delete"),
]
