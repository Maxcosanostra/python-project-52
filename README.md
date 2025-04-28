<div align="center">

[![Actions Status](https://github.com/Maxcosanostra/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Maxcosanostra/python-project-52/actions)
[![Live demo – Render](https://img.shields.io/badge/Live%20demo-Render-00c7d6?logo=render&logoColor=white)](https://python-project-52-q6c1.onrender.com)

</div>

# Менеджер задач&nbsp;&nbsp;&nbsp;<img src="https://user-images.githubusercontent.com/74038190/212284087-bbe7e430-757e-4901-90bf-4cd2ce3e1852.gif" alt="animation" align="left" width="40"/>
Таск-менеджер на Django, реализующий CRUD для пользователей, статусов, меток и задач, а также интеграцию с Rollbar для сбора ошибок.


## Демо

Чтобы быстро посмотреть приложение в действии, нажмите на бейдж сверху или откройте [сайт](https://python-project-52-q6c1.onrender.com) — регистрация свободная.


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
5. Примените миграции:
   ```bash
   python manage.py migrate
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
- Environment Variables: SECRET_KEY из .env
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





