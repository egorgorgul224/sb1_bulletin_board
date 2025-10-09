from rest_framework.pagination import PageNumberPagination


class AdListPaginator(PageNumberPagination):
    """Пагинатор для вывода списка объявлений. Выводит 4 элемента на страницу."""

    page_size = 4
    page_size_query_param = "page_size"
