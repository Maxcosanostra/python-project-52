# Менеджер задач

Таск-менеджер на Django, реализующий CRUD для пользователей, статусов, меток и задач, а также интеграцию с Rollbar для сбора ошибок.


### Hexlet tests and linter status:
[![Actions Status](https://github.com/Maxcosanostra/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Maxcosanostra/python-project-52/actions)


## Описание проекта

В данном проекте:
- Регистрация и аутентификация пользователей.
- CRUD (создание, чтение, обновление, удаление) для:
  - Пользователей
  - Статусов задач
  - Меток (labels)
  - Задач (tasks) с привязкой к статусу, исполнителю, меткам и автору.
- Фильтрация списка задач по статусу, исполнителю, меткам и автору.
- Flash-сообщения при успешных операциях.
- Полная русификация интерфейса.
- Сбор ошибок в Rollbar.

## Требования

- Python 3.11+
- Django 3.2+
- Django-bootstrap5
- Django-filter
- dj-database-url
- Gunicorn
- Python-dotenv
- Rollbar

## 📥 Установка и запуск

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Maxcosanostra/python-project-52
   cd python-project-52
   ```
2. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Создайте файл `.env` на основе примера:
   ```bash
   cp .env.example .env
   ```
4. Откройте `.env` и заполните:
   ```dotenv
   DJANGO_SECRET_KEY=<ваш секретный ключ>
   DEBUG=True
   ROLLBAR_ACCESS_TOKEN=<ваш токен Rollbar>
   ```
5. Примените миграции и создайте суперпользователя:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

## Тестирование

Запуск тестов:
```bash
python manage.py test
```

##  Интеграция с Rollbar

1. Зарегистрируйтесь на [Rollbar](https://rollbar.com/).
2. Создайте проект, получите **access token** с правом записывать (write).
3. Вставьте `ROLLBAR_ACCESS_TOKEN` в ваш файл `.env`.
4. Проект автоматически инициализирует Rollbar через `settings.py`.
5. Ошибки в продакшен-среде будут отправляться в ваш аккаунт Rollbar.

##  Деплой на Render

Render.com позволяет быстро развернуть Django‑приложение.

1. Зарегистрируйтесь или войдите в Render.
2. Создайте новый **Web Service**.
3. Подключите ваш GitHub‑репозиторий **python-project-52**.

#### В настройках сервиса установите:
- Build Command: make build
- Start Command: make render-start
4. Сохраните и дождитесь успешного билда и деплоя.  
   Ваш сервис будет доступен по URL, указанному Render.



## Что коммитить и что не желательно

**Разрешено коммитить:**
- `settings.py` (читает секреты из окружения)
- `.env.example` (с примером переменных)
- `README.md`, `requirements.txt`, исходный код, миграции, шаблоны, статические файлы

**Запрещено коммитить:**
- Реальный файл `.env` с вашими секретами
- Живые значения `SECRET_KEY` или `ROLLBAR_ACCESS_TOKEN` в коде
- `db.sqlite3` и другие файлы баз данных
- Медиа‑файлы и пользовательские загрузки

---





