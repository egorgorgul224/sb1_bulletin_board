from django.contrib import admin

from .models import Ad, Review


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Админ панель по объявлениям. Поля для отображения: title, price, created_at, author. Поле для фильтра: author,
    created_at. Поле для поиска: title."""

    list_display = ("title", "price", "author", "created_at")
    list_filter = ("author", "created_at")
    search_fields = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админ панель по отзывам. Поля для отображения: text, created_at, author. Поле для фильтра: author, created_at.
    Поле для поиска: text."""

    list_display = ("text", "author", "created_at")
    list_filter = ("author", "created_at")
    search_fields = ("text",)
