from rest_framework import serializers

from ads.models import Ad, Review


class AdSerializer(serializers.ModelSerializer):
    """Сериализация модели Ad. Предоставлен доступ ко всем полям, кроме author."""

    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ["id", "review_count", "title", "price", "description", "created_at"]

    def get_review_count(self, obj):
        """Метод для подсчета количества отзывов в объявлении. 'ad_reviews' - related_name поля 'ad' модели Review."""

        return obj.ad_reviews.count()


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация модели Review. Предоставлен доступ ко всем полям, кроме author, created_at."""

    class Meta:
        model = Review
        exclude = ["author", "created_at"]
