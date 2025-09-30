from rest_framework import generics

from ads.models import Ad, Review
from ads.serializers import AdSerializer, ReviewSerializer


class AdCreateAPIView(generics.CreateAPIView):
    """Класс generics модели Ad для создания объявления."""

    serializer_class = AdSerializer

    def perform_create(self, serializer):
        """Метод добавляет в поле author пользователя, который создает объявление."""

        habit = serializer.save()
        habit.author = self.request.user
        habit.save()


class AdListAPIView(generics.ListAPIView):
    """Класс generics модели Ad для вывода списка объявлений."""

    serializer_class = AdSerializer

    def get_queryset(self):
        """Функция для получения списка объявлений. Если админ - то все, пользователь - только свои."""

        user = self.request.user
        if user.is_superuser:
            return Ad.objects.all()
        else:
            return Ad.objects.filter(author=self.request.user.id)


class AdRetrieveAPIView(generics.RetrieveAPIView):
    """Класс generics модели Ad для вывода информации об объявлении."""

    serializer_class = AdSerializer
    queryset = Ad.objects.all()


class AdUpdateAPIView(generics.UpdateAPIView):
    """Класс generics модели Ad для обновления информации объявления."""

    serializer_class = AdSerializer
    queryset = Ad.objects.all()


class AdDestroyAPIView(generics.DestroyAPIView):
    """Класс generics модели Ad для удаления объявления."""

    queryset = Ad.objects.all()


class ReviewCreateAPIView(generics.CreateAPIView):
    """Класс generics модели Review для создания отзыва."""

    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        """Метод добавляет в поле author пользователя, который добавляет отзыв."""

        review = serializer.save()
        review.author = self.request.user
        review.save()


class ReviewListAPIView(generics.ListAPIView):
    """Класс generics модели Review для вывода списка отзывов."""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Функция для получения списка отзывов. Если админ - то все, пользователь - только свои."""

        user = self.request.user
        if user.is_superuser:
            return Review.objects.all()
        else:
            return Review.objects.filter(author=self.request.user.id)


class ReviewRetrieveAPIView(generics.RetrieveAPIView):
    """Класс generics модели Review для вывода информации об отзыве."""

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class ReviewUpdateAPIView(generics.UpdateAPIView):
    """Класс generics модели Review для обновления информации об отзыве."""

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class ReviewDestroyAPIView(generics.DestroyAPIView):
    """Класс generics модели Review для удаления отзыва."""

    queryset = Review.objects.all()
