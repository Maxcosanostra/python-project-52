"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import index
# from .views import rollbar_test  # тестовая вьюшка

urlpatterns = [
    path('admin/', admin.site.urls),
    # # тестовая ссылка, по которой мы намеренно кинем exception:
    # path('rollbar/test-error/', rollbar_test, name='rollbar_test'),
    path('', index, name='index'),
    path('', include('task_manager.urls_users')),
    path('', include('task_manager.urls_statuses')),
    path('', include('task_manager.urls_tasks')),
    path('', include('task_manager.urls_labels')),
]
