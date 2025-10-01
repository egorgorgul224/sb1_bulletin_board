from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsAccountOwner
from users.serializers import RegisterUserSerializer, UserMinInfoSerializer, UserSerializer


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
    permission_classes = [
        IsAccountOwner,
    ]

    def get_serializer_class(self):
        """Метод для вывода необходимого сериализатора. Если пользователь 'staff' или 'admin' - выводится вся
        информация через UserSerializer, иначе только часть информации через UserMinInfoSerializer."""

        user = self.request.user
        if user.is_staff or user.role == "admin":
            return UserSerializer
        return UserMinInfoSerializer
