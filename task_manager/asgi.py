"""
ASGI config for task_manager project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import dotenv
from django.core.asgi import get_asgi_application

# Подгружаем переменные из .env
dotenv.load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

application = get_asgi_application()
