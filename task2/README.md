### [Что это за TASK2?] :smiley_cat: 
TASK2 -это API реализованный на FastAPI (простите за тавтологию ещё раз:), с возможностью регистрации, авторизации по JWT-токену через cookie transport.
С помощью этого сервиса возможно преобразование аудиозаписей из формата wav в формат mp3. Каждый авторизованный
пользователь может загружать свои аудиозаписи и скачивать их в преобразованном виде!

### Как запустить? :space_invader:
Проект можно запустить, используя Docker для этого:

Клонировать репозиторий:

```
git clone git@github.com:Artem4es/FASTAPI.git
```

Перейти в папку infra и создать файл .env :
```
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres

DB_HOST_TEST=db
DB_PORT_TEST=5432
DB_NAME_TEST=testbase
DB_USER_TEST=postgres
DB_PASS_TEST=postgres
```

Cоздать и запустить контейнеры из папки infra:
```
docker compose up -d
```

Применить миграции (они уже созданы) через alembic:

```
docker compose exec --workdir /app backend alembic upgrade heads
```


### Начало взаимодействия с API :old_key:
После запуска проекта для получения полного доступа к интерфейсу необходимо: 

1. Создать нового пользователя, отправив POST запрос на эндпоинт http://localhost/auth/register в формате:

```
{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "username": "string"
}
```

2. Получить JWT-токен для авторизации, отправив POST запрос на эндпоинт http://localhost/auth/jwt/login в формате: 
```
{
"username": "ваш email",
"password": "ваш пароль"
}
```
Токен будет передан в cookie. Cрок действия 24ч после чего его необходимо обновить.

### Преобразование wav в mp3
Нужно отправить файл с расширением .wav методом POST на эндпоинт http://localhost/uploadfile/
В теле ответа при удачном запросе придёт ссылка на скачивание преобразованного файла.
При переходе по ссылке начнётся скачивание файла.


### Документация проекта: :blue_book:
После запуска проекта доступная документация Swagger и Redoc по адресам:
http://localhost/docs/
или тут
http://localhost/redoc/
