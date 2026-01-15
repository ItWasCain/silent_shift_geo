# Тестовое задание - Геолокационный сервис

## Общее описание проекта
Проект представляет собой REST API для работы с геолокационными точками и сообщениями. Пользователи могут создавать точки на карте, оставлять к ним сообщения и осуществлять поиск по радиусу. Данные передаются в формате JSON.

## Основные возможности
- Создание, чтение, обновление и удаление геолокационных точек
- Привязка сообщений к точкам
- Поиск точек и сообщений в заданном радиусе
- JWT-аутентификация
- Регистрация пользователей

## Как запустить проект

### 1. Клонировать репозиторий и перейти в него
```
git clone https://github.com/ItWasCain/silent_shift_geo.git
cd silent_shift_geo/infra/
```

### 2. Создать и настроить .env файл

```
cp .env.example .env
```

Отредактируйте .env файл в папке /infra, установите свои значения.

### 3. Запустить проект в Docker
```
docker compose up -d --build
```
### 4. Создать суперпользователя (опционально)
```
docker compose exec backend python manage.py createsuperuser
```
### 5. Собрать статику (если нужно)
```
docker compose exec backend python manage.py collectstatic --no-input
```
### 6. Проект будет доступен по адресам:
API: http://localhost/api/
Админ-панель: http://localhost/admin/


## API Документация
### Аутентификация
Регистрация пользователя
```
POST http://localhost:8000/api/auth/register/
Content-Type: application/json

{
    "username": "testuser",
    "password": "testpassword123",
    "email": "test@example.com"
}
```
Получение JWT токена
```
POST http://localhost:8000/api/auth/token/
Content-Type: application/json

{
    "username": "testuser",
    "password": "testpassword123"
}
```
Обновление токена
```
POST http://localhost:8000/api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "ваш_refresh_токен"
}
```
Проверка токена
```
POST http://localhost:8000/api/auth/token/verify/
Content-Type: application/json

{
    "token": "ваш_access_токен"
}
```
### Точки (Points)
Создание точки
```
POST http://localhost:8000/api/points/
Authorization: Bearer ваш_access_токен
Content-Type: application/json

{
    "name": "Красная площадь",
    "latitude": 55.7539,
    "longitude": 37.6208
}
```
Получение всех точек
```
GET http://localhost:8000/api/points/
Authorization: Bearer ваш_access_токен
```
Получение конкретной точки
```
GET http://localhost:8000/api/points/{id}/
Authorization: Bearer ваш_access_токен
```
Поиск точек в радиусе
```
POST http://localhost:8000/api/points/search/
Authorization: Bearer ваш_access_токен
Content-Type: application/json

{
    "latitude": 55.7539,
    "longitude": 37.6208,
    "radius_km": 10.0
}
```
Обновление точки
```
PUT http://localhost:8000/api/points/{id}/
Authorization: Bearer ваш_access_токен
Content-Type: application/json

{
    "name": "Обновленное название",
    "latitude": 55.7540,
    "longitude": 37.6210
}
```
Частичное обновление точки
```
PATCH http://localhost:8000/api/points/{id}/
Authorization: Bearer ваш_access_токен
Content-Type: application/json

{
    "name": "Меняем только название"
}
```
Удаление точки
```
DELETE http://localhost:8000/api/points/{id}/
Authorization: Bearer ваш_access_токен
```
### Сообщения
Создание сообщения
```
POST http://localhost:8000/api/messages/points/messages/
Authorization: Bearer ваш_access_токен
Content-Type: application/json

{
    "point": 1,
    "content": "Это тестовое сообщение для точки"
}
```
Получение всех сообщений
```
GET http://localhost:8000/api/messages/
Authorization: Bearer ваш_access_токен
```
Получение конкретного сообщения
```
GET http://localhost:8000/api/messages/{id}/
Authorization: Bearer ваш_access_токен
```
Поиск сообщений в радиусе
```
POST http://localhost:8000/api/messages/search/
Authorization: Bearer ваш_access_токен
Content-Type: application/json

{
    "latitude": 55.7539,
    "longitude": 37.6208,
    "radius_km": 5.0
}
```
Обновление сообщения
```
PUT http://localhost:8000/api/messages/{id}/
Authorization: Bearer ваш_access_токен
Content-Type: application/json

{
    "content": "Обновленный текст сообщения"
}
```
Удаление сообщения
```
DELETE http://localhost:8000/api/messages/{id}/
Authorization: Bearer ваш_access_токен
```

## Важные моменты
Все запросы (кроме регистрации и получения токена) требуют Authorization Header
Для создания точек/сообщений нужно сначала получить токен
ID точек и сообщений смотрите в ответах на GET-запросы
Удаление/обновление доступно только автору или администратору
Координаты должны быть в диапазонах:
Широта (latitude): от -90.0 до 90.0
Долгота (longitude): от -180.0 до 180.0

## Технологии
Backend: Python 3.11+, Django 4.2+, Django REST Framework 3.14+
База данных: PostgreSQL 15+ с PostGIS 3.3+
Аутентификация: JWT (Django REST Framework Simple JWT)
Геоданные: Django GIS, GEOS, GDAL
Контейнеризация: Docker, Docker Compose
Веб-сервер: Nginx
Формат данных: JSON

## Разработчик
Никита Песчанов https://github.com/ItWasCain
