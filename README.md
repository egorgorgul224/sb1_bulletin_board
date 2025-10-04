# Дипломный проект "SB1 доска объявлений"

---

## Оглавление

<a id="content"></a>

1. [Описание](#description)
2. [Установка и настройка проекта](#instruction)
3. [Структура проекта](#structure)
4. [Приложения](#apps)
   - [Приложение Ads](#ads_app)
     - [Модели](#ads_models) 
     - [Контроллеры и ссылки](#ads_controllers)
     - [Сериализация](#ads_serialize)
     - [Пагинаторы](#ads_paginators)
   - [Приложение Users](#users_app)
     - [Модели](#users_models) 
     - [Контроллеры и ссылки](#users_controllers)
     - [Сериализация](#users_serialize)
     - [Классы разрешений](#users_permissions)
5. [Тестирование](#tests)
6. [Запуск и тестирование проекта, документация](#launch)
7. [Запуск и тестирование с помощью Docker Compose](#docker)
8. [Лицензия](#license)

---

## Описание<a id="description"></a>

В проекте реализована backend-часть для сайта объявлений.

---

## Установка и настройка проекта<a id="instruction"></a>

1. Клонируйте репозиторий:

```
git clone https://github.com/username/project-x.git
```

2. Перейдите в директорию проекта:

```
cd ваш_проект
```

3. Установите зависимости проекта:

```
poetry install
```

4. Зайдите в файл .env.example и следуйте инструкциям из него.

---

## Структура проекта<a id="structure"></a>

```
.
├── config
│     ├── asgi.py, settings.py, urls.py, wsgi.py необходимые модули для работы приложения
├──ads  - приложение на django
│ ├── migrations - папка с миграциями
│ ├── admin.py, apps.py, models.py, paginators.py, serializers.py, tests.py, urls.py, views.py - модули для работы
приложения
├──config  - настройки django
├──tests  - тесты приложений
│ ├── ad_reviews - пакет с фикстурами, тестами модулей Ad, Review
│ ├── user - пакет с фикстурами, тестами модуля User
├── users - приложение на django
│ ├── management
│     ├── commands - папка с командами
│         ├── createadmin - команда для создания суперпользователя(админа)
│ ├── migrations - папка с миграциями
│ ├── admin.py, apps.py, models.py, permissions.py, serializers.py, tests.py, urls.py, views.py - модулидля работы
приложения
├── .env.example - env экземпляр для доступа к закрытым данным
├── .flake8
├── .gitignore
├── docker-compose.yml - контейнер проекта в docker hub
├── Dockerfile - файл для создания образа
├── manage.py
├── pyproject.toml
├── poetry.lock
├── pytest.ini - файл настройки pytest
├── requirements.txt - файл с зависимостями
└── README.md
```

---

## Приложения<a id="apps"></a>

В проекте реализовано 2 приложения:
1. **ads**: приложение для ведения объявлений и отзывов.
2. **users**: приложения для создания/редактирования/просмотра и удаления пользователя.

---

## Приложение Ads <a id="ads_app"></a>

Приложение **ads** создано для создания/редактирования/удаления и ведения объявлений и отзывов.

Ниже будут описаны модели, контроллеры + ссылки, сериализации.

### Модели<a id="ads_models"></a>

В приложении созданы следующие модели:
- Ad - модель объявление. Содержит поля title, price, description, author, created_at.
- Review - модель отзыв. Содержит поля text, author, ad, created_at.

### Контроллеры и ссылки<a id="ads_controllers"></a>

1. Контроллеры модели **Ad**.
   - Контроллер AdCreateAPIView для создания объявления.
   - Контроллер AdListAPIView для вывода списка своих объявлений(если admin, то всех).
   - Контроллер AdRetrieveAPIView для вывода информации об объявлении.
   - Контроллер AdUpdateAPIView для обновления информации объявления.
   - Контроллер AdDestroyAPIView для удаления объявления.

```
Ссылка для контроллера AdCreateAPIView: адрес/ad/create/
Ссылка для контроллера AdListAPIView: адрес/ads/
Ссылка для контроллера AdRetrieveAPIView: адрес/ad/id_объявления/detail/
Ссылка для контроллера AdUpdateAPIView: адрес/ad/id_объявления/update/
Ссылка для контроллера AdDestroyAPIView: адрес/ad/id_объявления/delete/
```

2. Контроллеры модели **Review**.
   - Контроллер ReviewCreateAPIView для создания отзыва.
   - Контроллер ReviewListAPIView для вывода списка отзывов.
   - Контроллер ReviewRetrieveAPIView для вывода информации об отзыве.
   - Контроллер ReviewUpdateAPIView для обновления информации отзыва.
   - Контроллер ReviewDestroyAPIView для удаления отзыва.

```
Ссылка для контроллера ReviewCreateAPIView: адрес/review/create/
Ссылка для контроллера ReviewListAPIView: адрес/ad/id_объявления/reviews/
Ссылка для контроллера ReviewRetrieveAPIView: адрес/review/id_отзыва/detail/
Ссылка для контроллера ReviewUpdateAPIView: адрес/review/id_отзыва/update/
Ссылка для контроллера ReviewDestroyAPIView: адрес/review/id_отзыва/delete/
```

### Сериализация<a id="ads_serialize"></a>

Реализованы следующие сериализации:
1. **AdSerializer** - сериализация модели Ad. Предоставлен доступ ко всем полям, кроме author.
2. **ReviewSerializer** - сериализация модели Review. Предоставлен доступ ко всем полям, кроме author, created_at.

### Пагинаторы<a id="ads_paginators"></a>

Реализованs следующие пагинаторы:
1. **AdListPaginator** - пагинатор для вывода списка объявлений. Выводит 4 элемента на страницу.

---

## Приложение User <a id="users_app"></a>

Приложение **user** создано для регистрации/авторизации/редактирования/просмотра и удаления пользователя.

Ниже будут описаны модели, контроллеры + ссылки, сериализации.

### Модели<a id="users_models"></a>

В приложении созданы следующие модели:
- User - модель пользователь. Содержит поля email, role, phone, image, token.

### Контроллеры и ссылки<a id="users_controllers"></a>

1. Контроллеры модели **User**.
   - Контроллер UserCreateAPIView для регистрации/создания пользователя.
   - Контроллер UserListAPIView для вывода списка пользователей.
   - Контроллер UserRetrieveAPIView для вывода информации о пользователе.
   - Контроллер UserUpdateAPIView для обновления информации о пользователе.
   - Контроллер UserDestroyAPIView для удаления пользователя.

```
Ссылка для контроллера UserCreateAPIView: адрес/register/
Ссылка для контроллера авторизации и получения токена TokenObtainPairView: адрес/login/
Ссылка для контроллера обновления токена TokenRefreshView: адрес/token/refresh/
Ссылка для контроллера UserListAPIView: адрес/users/
Ссылка для контроллера UserRetrieveAPIView: адрес/user/id_пользователя/detail/
Ссылка для контроллера UserUpdateAPIView: адрес/user/id_пользователя/update/
Ссылка для контроллера UserDestroyAPIView: адрес/user/id_пользователя/delete/
```

### Сериализация<a id="users_serialize"></a>

Реализованы следующие сериализации:
1. **UserSerializer** - сериализатор для модели User. В Meta класс предоставлен доступ к полям: first_name, last_name,
phone, email, date_joined.
2. **UserMinInfoSerializer** - Дополнительная сериализация модели User для обычных пользователей. Предоставлен доступ
к полям: last_name, first_name, date_joined.
3. **RegisterUserSerializer** - сериализатор для контроллера UserCreateAPIView. Используется для регистрации/создания
пользователя. Предоставлен доступ к полям: email.

### Классы разрешений<a id="users_permissions"></a>

Реализованы следующие разрешения:
1. **IsAdReviewOwner** - проверяет, что пользователь является создателем объявления или отзыва. Если владелец -
возвращает True, иначе False.
2. **IsAccountOwner** - проверяет, что пользователь является владельцем аккаунта. Если владелец - возвращает True,
иначе False.
3. **IsAdmin** - проверяет, что пользователь является админом. Если админ - возвращает True, иначе False.

---

## Тестирование<a id="tests"></a>

Приложения протестированы с помощью pytest:
1. Функционал модели и контроллеров User.
2. Функционал модели и контроллеров Ad.
3. Функционал модели и контроллеров Review.

---

## Запуск и тестирование проекта, документация<a id="launch"></a>

1. После установки и настройки проекта в консоль введите python/python3 manage.py runserver для запуска сервера.
2. Создание/редактирование/просмотр/удаление моделей проводится в Postman.
3. Для просмотра документации введите в адресной строке:
```
http://127.0.0.1:8000/swagger/ - документация в swagger
http://127.0.0.1:8000/redoc/ - документация в redoc
```

---

## Запуск и тестирование с помощью Docker Compose<a id="docker"></a>

С помощью Docker Compose можно запустить все необходимые для проекта сервисы в одной оболочке(веб-приложение, базу
данных(PostgreSQL) и др.).

Запуск:
1. Клонируйте репозиторий:
```
git clone https://github.com/username/project-x.git
```
2. Перейдите в директорию проекта:
```
cd ваш_проект
```
3. Зайдите в файл .env.example и следуйте инструкциям из него.
4. Установите Docker.
5. Введите команду для создания и запуска Docker Compose в фоновом режиме.
```
docker-compose up -d --build
```
6. Проверить работоспособность Docker Compose можно:
- проверить сервер по адресу:
```
http://localhost:8000/
или
http://127.0.0.1:8000/
```
- проверить документацию или admin-панель:
```
http://127.0.0.1:8000/swagger/
и
http://127.0.0.1:8000/admin/
```
- для добавления админа и входа в базу данных используйте команды:
```
создание админа:
docker-compose run web python manage.py createadmin

входа в базу данных:
docker exec -it django_rest_homework-db-1  psql -U postgres materials

проверка всех таблиц в базе данных:
\dt

пример для проверки пользователей:
SELECT * FROM users_user;
```
- ввести в терминал команду, запущенные команды будут иметь status "Up":
```
docker-compose ps
```
- ввести в терминал команду для просмотра логов по каждому сервису:
```
docker-compose logs
```
7. Для остановки и/или удаления используйте команду:
```
docker-compose stop
или с удалением контейнера:
docker-compose down
```

---

## Лицензия<a id="license"></a>

Этот проект лицензирован по [лицензии MIT](LICENSE).

##### [Оглавление](#content)