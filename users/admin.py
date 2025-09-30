from django.contrib import admin

from users.models import User


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    """Админ панель с пользователями. Поля для отображения: email, last_name, first_name, phone. Поля для поиска:
    email, phone."""

    list_display = ("email", "last_name", "first_name", "phone")
    search_fields = ("email", "phone")
