import django_filters
from django import forms
from .models import Task


class TaskFilter(django_filters.FilterSet):
    my_tasks = django_filters.BooleanFilter(
        method='filter_my_tasks',
        widget=forms.CheckboxInput,
        label="Только мои задачи"
    )

    class Meta:
        model = Task
        fields = {
            'status': ['exact'],
            'assigned_to': ['exact'],
            'labels': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request", None)
        super().__init__(*args, **kwargs)

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
