from rest_framework.permissions import BasePermission


class IsAdReviewOwner(BasePermission):
    """Класс проверяет, что пользователь является создателем объявления или отзыва. Если владелец - возвращает True,
    иначе False."""

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsAccountOwner(BasePermission):
    """Класс проверяет, что пользователь является владельцем аккаунта. Если владелец - возвращает True, иначе False."""

    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        return False
