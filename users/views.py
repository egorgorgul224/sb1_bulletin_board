import secrets

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.permissions import IsAccountOwner
from users.serializers import RegisterUserSerializer, UserMinInfoSerializer, UserSerializer
from users.services import send_password_reset_email


class UserCreateAPIView(generics.CreateAPIView):
    """Класс generics модели User для регистрации/создания пользователя."""

    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Класс generics модели User для вывода информации о пользователе."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        IsAccountOwner,
    ]


class UserUpdateAPIView(generics.UpdateAPIView):
    """Класс generics модели User для обновления информации о пользователе."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        IsAccountOwner,
    ]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Класс generics модели User для удаления пользователя."""

    queryset = User.objects.all()
    permission_classes = [
        IsAccountOwner,
    ]


class UserListAPIView(generics.ListAPIView):
    """Класс generics модели User для вывода списка пользователей(всех, кроме администраторов)."""

    serializer_class = UserSerializer
    queryset = User.objects.filter(is_staff=False)

    def get_serializer_class(self):
        """Метод для вывода необходимого сериализатора. Если пользователь 'staff' - выводится вся информация через
        UserSerializer, иначе только часть информации через UserMinInfoSerializer."""

        user = self.request.user
        if user.is_staff:
            return UserSerializer
        return UserMinInfoSerializer


class UserResetPassword(APIView):
    """Контроллер для сброса пароля и отправки сообщения на email пользователя."""

    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:

        email = request.data.get("email")
        try:
            user = get_object_or_404(User, email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(str(user.pk)))
            token = secrets.token_hex(16)
            user.token = token
            user.save()
            send_password_reset_email(email, uidb64, token)
            return Response({"detail": "Ссылка для сброса пароля отправлена."}, status=status.HTTP_200_OK)
        except Http404:
            return Response({"detail": "Пользователь с данным email не найден."}, status=status.HTTP_404_NOT_FOUND)


class UserResetPasswordConfirm(APIView):
    """Контроллер для подтверждения сброса пароля и установки нового пароля."""

    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        """"""
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
            if user.token != token:
                return Response({"detail": "Передан неверный токен."}, status=status.HTTP_403_FORBIDDEN)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Пароль успешно изменен."}, status=status.HTTP_200_OK)
        except Http404:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)
