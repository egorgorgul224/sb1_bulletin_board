from rest_framework import serializers

from ads.models import Ad, Review


class AdSerializer(serializers.ModelSerializer):
    """Сериализация модели Ad. Предоставлен доступ ко всем полям, кроме author."""

    class Meta:
        model = Ad
        exclude = ["author"]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация модели Ad. Предоставлен доступ ко всем полям, кроме author, created_at."""

    class Meta:
        model = Review
        exclude = ["author", "created_at"]
