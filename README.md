# API кадровых потребностей регионов

Лёгкий REST API на FastAPI с mock-репозиторием в памяти. Данные в примере вымышлены и используются только для демонстрации.

## Требования

- Python 3.11 или новее
- [uv](https://docs.astral.sh/uv/)

## Установка и запуск

```bash
uv sync
cp .env.example .env
```

Задайте собственный секрет в `.env`:

```dotenv
APP_TOKEN=your-secret-token
```

Запустите сервер:

```bash
uv run uvicorn app.main:app --reload
```

API будет доступно по адресу `http://127.0.0.1:8000`.

## Запуск в Docker

Соберите образ из корня проекта:

```bash
docker build -t regional-staffing-api .
```

Создайте `.env` по `.env.example`, укажите собственный `APP_TOKEN`, затем запустите контейнер:

```bash
docker run --rm --name regional-staffing-api \\
  --env-file .env \\
  -p 8000:8000 \\
  regional-staffing-api
```

## Запрос

```bash
curl -X POST http://127.0.0.1:8000/api/v1/staffing/needs \
  -H 'Content-Type: application/json' \
  -H 'x-app-token: your-secret-token' \
  -d '{"region":"Москва"}'
```

Успешный ответ содержит показатели по годам и метрики `total`, `replacement` и `additional`. Доступны mock-данные для Москвы, Санкт-Петербурга и Республики Татарстан. Для неизвестного региона API возвращает `404`, при отсутствующем или неверном токене — `401`, при некорректном теле — `422`.

## Тесты

```bash
uv run pytest
```
