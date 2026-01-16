# Video API
## Описание проекта
Video API - это REST‑сервис для управления видеозаписями с камер наблюдения. Поддерживает создание, получение и обновление статуса видео.

## Основные возможности
- Создание записей о видео;
- Получение списка видео с фильтрацией;
- Получение конкретного видео по ID;
- Обновление статуса видео;
- Валидация данных;
- Автоматическое управление схемой БД;
- Интеграция с PostgreSQL;
- Документация API;
- Обработка ошибок.

## Используемые технологии
- Python 3.10.11
- FastAPI 0.128.0 (для построения REST‑API с автоматической документацией (Swagger UI), валидацией данных и асинхронной обработкой)
- Pydantic 2.12.5 (для описания схем запросов/ответов, валидации входных данных и преобразования типов)
- SQLAlchemy 2.0.45 (ORM для взаимодействия с PostgreSQL)
- PostgreSQL 15.15-1
- Uvicorn 0.40.0 (ASGI‑сервер)
- Docker + docker-compose

## Локальный запуск проекта
- Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone git@github.com:ivanlbdv/video-api.git
cd video-api
```

- Убедитесь, что в папке проекта есть:

```
docker-compose.yml
Dockerfile
requirements.txt
```

- Соберите и запустите контейнеры:

```bash
docker-compose up -d --build
```

- Проверьте статус контейнеров:

```bash
docker-compose ps
```

Ожидаемый результат: статус 'running' для app и db

- Откройте документацию API

Перейдите в браузере по адресу:
http://localhost:8000/docs

## Основные команды
- Управление контейнерами:
    - остановка

    ```bash
    docker-compose down
    ```

    - перезапуск

    ```bash
    docker-compose restart
    ```

    - пересборка (при изменении кода)

    ```bash
    docker-compose up -d --build
    ```

- Просмотр логов:
    - API

    ```bash
    docker-compose logs app
    ```

    - БД

    ```bash
    docker-compose logs db
    ```

## Примеры запросов
- Создание видео

```bash
curl -X POST "http://localhost:8000/videos" \
 -H "Content-Type: application/json" \
 -d '{
 "video_path": "/storage/camera1/2024-01-15_10-30-00.mp4",
 "start_time": "2024-01-15T10:30:00",
 "duration": "PT1H",
 "camera_number": 1,
 "location": "Entrance"
 }
```

- Получение всех видео

```bash
curl "http://localhost:8000/videos"
```

- Получение видео по ID

```bash
curl "http://localhost:8000/videos/1"
```

- Обновление статуса видео

```bash
-X PATCH "http://localhost:8000/videos/1/status" \
 -H "Content-Type: application/json" \
 -d '{"status": "transcoded"}'
```

## Автор:
Иван Лебедев
https://github.com/ivanlbdv
