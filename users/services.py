from django.core.mail import send_mail

from config import settings


def send_password_reset_email(email: str, uidb64: str, token: str) -> None:
    """Функция отправляет сообщение сброса пароля на почту пользователя."""

    subject = "Восстановление пароля"
    message = f"{settings.URL}reset_password_confirm/{uidb64}/{token}"
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,
    )
