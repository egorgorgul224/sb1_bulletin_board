from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Модель пользователь. Содержит поля email, phone, avatar."""

    ROLE_CHOICES = [("user", "Пользователь"), ("admin", "Администратор")]

    username = None
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите email")

    role = models.CharField(max_length=5, default="user", choices=ROLE_CHOICES, verbose_name="Роль пользователя")
    phone = models.CharField(max_length=35, verbose_name="Телефон", blank=True, null=True)
    image = models.ImageField(upload_to="avatars/", verbose_name="Аватар", blank=True, null=True)
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}, {self.is_active}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]
