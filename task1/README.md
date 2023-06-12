### [Что это за FASTAPI?] :smiley_cat: 
TASK1 -это API реализованный на FastAPI (простите за тавтологию) для получения списка вопросов для викторин. Вы отправляете количество вопросов
и в ответ приходят вопросы с ответами от внешнего API.

### Как запустить? :space_invader:
Проект можно запустить, используя Docker для этого:

Клонировать репозиторий:

```
git clone git@github.com:Artem4es/FASTAPI.git
```
Перейти в папку /task1

```
cd task1
```
Создать файл .env с переменными окружения и содержимым:

```
REAL_DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres
POSTGRES_PASSWORD=postgres
```

Cоздать и запустить контейнеры:

```
docker compose up -d
```

Применить миграции (они уже созданы) через alembic:

```
docker compose exec backend alembic upgrade heads 
```


### Начало взаимодействия с API :old_key:
После запуска проекта для получения списка вопросов нужно отправить POST запрос на эндпоинт http://localhost в формате:

```
{
  "questions_num": количество вопросов
}
```

В ответ придёт последний сохранённый в БД вопрос в формате:
```
{
  "id": 30593,
  "answer": "men",
  "question": "According to Mark 1:17, Jesus told his disciples to leave their jobs to become \"fishers of\" these",
  "created_at": "2022-12-30T18:50:11.310000+00:00"
}
```
Все остальные вопросы сохраняются в БД.


### Документация проекта: :blue_book:
После запуска проекта доступная документация Swagger и Redoc по адресам:
http://localhost/docs/
или тут
http://localhost/redoc/