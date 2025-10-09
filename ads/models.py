from django.db import models

from config import settings


class Ad(models.Model):
    """Модель объявление. Содержит поля title, price, description, author, created_at."""

    title = models.CharField(max_length=100, verbose_name="Название товара")
    price = models.PositiveBigIntegerField(verbose_name="Цена товара")
    description = models.TextField(null=True, blank=True, verbose_name="Описание товара")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="ads", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}: {self.title} - {self.price}"

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["created_at"]


class Review(models.Model):
    """Модель отзыв. Содержит поля text, author, ad, created_at."""

    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="author_reviews", blank=True, null=True
    )
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="ad_reviews", verbose_name="Объявление")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at}: {self.ad} - {self.author}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["created_at"]
