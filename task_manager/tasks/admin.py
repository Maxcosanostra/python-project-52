from django.contrib import admin
from ..tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "author", "created_at")
    list_filter = ("status", "author", "assigned_to")
    search_fields = ("name", "description")
